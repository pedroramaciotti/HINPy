import pandas as pd
import numpy as np

from .link_group_class import LinkGroup
from .object_group_class import ObjectGroup
from .hin_functions import *
from hinpy.rs.hin_rs import *
from hinpy.diversity.truediversity import *
from hinpy.general import *


class HIN:
    """
    HIN: Heterogeneous Information Network Object

    """

    def __init__(self,filename=None,table=None,name=None,inverse_relations=True):

        # If there is no table, create from file
        if table is None:
            if filename is None:
                raise ValueError('HIN object has to be created from a table or from a file.')
            columns=['relation',
                    'start_group','start_object',
                    'end_group','end_object',
                    'value','timestamp']
            table=pd.read_csv(filename,sep=',',header=None,names=columns,low_memory=False)

        # Cheking the table
        table = CheckTable(table)

        # TODO: Aggregation of multi edges: None, Average, Sum

        # Filling the fields
        self.table = table
        self.name = name
        self.info = {}

        # Building Object and Link Groups from Table
        self.ReBuildObjectGroupsFromTable()
        self.ReBuildLinkGroupsFromTable()

        if inverse_relations:
            for relation_name in self.table.relation.unique():
                self.CreateInverseLinkGroup(relation_name)

        return;

    ###########################################
    # Functions Changing Link Groups          #
    ###########################################

    def CreateInverseLinkGroup(self,existing_relation_name,new_relation_name=None):
        # Checking that the relation exists
        if existing_relation_name not in self.table.relation.unique():
            raise ValueError('Relation %s does not exist.'%existing_relation_name)
        # Selecting the sub table of the relation to inverse
        subtable=self.table[self.table.relation==existing_relation_name].copy(deep=True)
        # Creating the new, appendable, subtable with the inverse relation
        new_subtable=pd.DataFrame(columns=subtable.columns)
        # Filling the entries of the new appendable subtable
        new_subtable.start_group=subtable.end_group
        new_subtable.start_object=subtable.end_object
        new_subtable.end_group=subtable.start_group
        new_subtable.end_object=subtable.start_object
        new_subtable.timestamp=pd.Timestamp('')
        new_subtable.value=''
        # Giving a name to the new relation
        if new_relation_name is None:
            new_subtable.relation='inverse_'+existing_relation_name
        else:
            new_subtable.relation=new_relation_name
        # Appending the table and changing the HIN
        self.table=self.table.append(new_subtable)
        new_link_group_id = self.GetNewLinkGroupID()
        sog_name=new_subtable.start_group.iloc[0]
        eog_name=new_subtable.end_group.iloc[0]
        self.link_group_dic[new_link_group_id] = LinkGroup(table=new_subtable,
                                                        name=new_subtable.relation.iloc[0],
                                                        id=new_link_group_id,
                                                        start_og=self.GetObjectGroup(sog_name),
                                                        end_og=self.GetObjectGroup(eog_name))

    def DeleteLinkGroup(self,relation_name):
        self.link_group_dic.pop(self.GetLinkGroupId(relation_name))
        self.table=self.table[self.table.relation!=relation_name]
        return;

    def MergeLinkGroups(self,relation_name, relation_name_to_merge,
                        new_relation_name=None, delete_merged_relation=False):
        # Get the group ids of the involved Link Groups
        og1_start = self.object_group_dic[self.GetLinkGroup(relation_name).start_id]
        og1_end   = self.object_group_dic[self.GetLinkGroup(relation_name).end_id]
        og2_start = self.object_group_dic[self.GetLinkGroup(relation_name_to_merge).start_id]
        og2_end   = self.object_group_dic[self.GetLinkGroup(relation_name_to_merge).end_id]
        # Check that relations start and end in the same Object Groups
        if (og1_start.id!=og2_start.id) or (og1_end.id!=og2_end.id):
            raise ValueError('Link Groups to be merged do not start and end in the same Object Groups.')
        # Subtable to be merged into a Link Group
        subtable = self.table[self.table.relation==relation_name].copy(deep=True)
        subtable_to_merge = self.table[self.table.relation==relation_name_to_merge].copy(deep=True)
        subtable_to_merge.loc[:,'relation'] = subtable.relation.iloc[0]
        merged_table=subtable.append(subtable_to_merge)
        self.table=self.table[self.table.relation!=relation_name]
        if new_relation_name is not None:
            merged_table.loc[:,'relation']=new_relation_name
        self.table=self.table.append(merged_table)
        lg_id = self.GetLinkGroupId(relation_name)
        self.link_group_dic[lg_id] = LinkGroup(table=merged_table,
                                                name=merged_table.relation.iloc[0],
                                                id=lg_id,
                                                start_og=og1_start,
                                                end_og=og1_end)
        if delete_merged_relation:
            self.DeleteLinkGroup(relation_name_to_merge)
        return;

    def CreateLinkGroupFromLinkGroup(self,relation_name,new_relation_name,condition_method):
        # Get the group ids of the Link Group
        og_start = self.object_group_dic[self.GetLinkGroup(relation_name).start_id]
        og_end  = self.object_group_dic[self.GetLinkGroup(relation_name).end_id]
        # Getting subtable of the Link Group
        subtable=self.table[self.table.relation==relation_name].copy(deep=True)
        # Applyting the condition
        subtable=subtable[subtable.value.apply(condition_method)]
        # Changing name
        subtable.relation = new_relation_name
        # Saving the new Link Group
        lg_id = self.GetNewLinkGroupID()
        self.link_group_dic[lg_id] = LinkGroup(table=subtable,
                                                name=subtable.relation.iloc[0],
                                                id=lg_id,
                                                start_og=og_start,
                                                end_og=og_end)
        return;

    def CreateLinkGroupFromRS(self,relation_name,new_relation_name,parameters):

        # Creating the recommendation table
        subtable = self.table[self.table.relation==relation_name].copy(deep=True)
        reco_table,report = HINRS(table=subtable,parameters=parameters,hin=self)
        reco_table.loc[:,'relation']= new_relation_name
        # Creating the new Link Group from the recommendation
        new_link_group_id = self.GetNewLinkGroupID()
        lg = self.GetLinkGroup(relation_name)
        self.link_group_dic[lg_id] = LinkGroup(table=reco_table,
                                                name=new_relation_name,
                                                id=new_link_group_id,
                                                start_og=lg.start_id,
                                                end_og=lg.end_id)
        return;

    ###########################################
    # Build Object and Link Groups from Table #
    ###########################################

    def ReBuildObjectGroupsFromTable(self):
        self.object_group_dic = {}
        object_group_id = 0
        for og_name in list(set(self.table.start_group.unique())|set(self.table.end_group.unique())):
            o_list = GetObjectsFromTableWithGroup(self.table,og_name)
            self.object_group_dic[object_group_id] = ObjectGroup(object_list=o_list,
                                                                name=og_name,
                                                                id=object_group_id)
            object_group_id+=1
        return;

    def ReBuildLinkGroupsFromTable(self):
        self.link_group_dic   = {}
        link_group_id=0
        for lg_name in self.table.relation.unique():
            sog_name = self.table[self.table.relation==lg_name].start_group.iloc[0]
            eog_name = self.table[self.table.relation==lg_name].end_group.iloc[0]
            self.link_group_dic[link_group_id] = LinkGroup(table=self.table[self.table.relation==lg_name],
                                                            name=lg_name,
                                                            id=link_group_id,
                                                            start_og=self.GetObjectGroup(sog_name),
                                                            end_og=self.GetObjectGroup(eog_name))
            link_group_id+=1
        return


    #####################################
    # HIN and Group Property Retrievers #
    #####################################

    # Get groups
    def GetObjectGroup(self,name):
        for og_id,og in self.object_group_dic.items():
            if og.name==name:
                return og;
        raise ValueError('Object Group %s not found'%name)

    def GetLinkGroup(self,name):
        for lg_id,lg in self.link_group_dic.items():
            if lg.name==name:
                return lg;
        raise ValueError('Link Group %s not found'%name)

    # Get Ids of groups
    def GetObjectGroupId(self,name):
        for og_id,og in self.object_group_dic.items():
            if og.name==name:
                return og_id;
        raise ValueError('Object Group %s not found'%name)

    def GetLinkGroupId(self,name):
        for lg_id,lg in self.link_group_dic.items():
            if lg.name==name:
                return lg_id;
        raise ValueError('Link Group %s not found'%name)

    # Get names of groups
    def GetObjectGroupsNames(self):
        return [og.name for og_id,og in self.object_group_dic.items()]

    def GetLinkGroupsNames(self):
        return [lg.name for lg_id,lg in self.link_group_dic.items()]

    # Get vacant id for new groups
    def GetNewLinkGroupID(self):
        return FirstAbsentNumberInList([k for k,v in self.link_group_dic.items()])

    def GetNewObjectGroupID(self):
        return FirstAbsentNumberInList([k for k,v in self.object_group_dic.items()])


    ##############################################
    # Path Proportional Abundances & Diversities #
    ##############################################

    # TODO: change to accept a probability distribution as input

    def GetPathStochasticMatrix(self,relation_list):
        path=CheckPath(relation_list)
        matrix=self.GetLinkGroup(path[0]).stochastic_matrix
        for relation in path[1:]:
            matrix=matrix*self.GetLinkGroup(relation).stochastic_matrix
        return matrix;

    def GetPathProportionalAbundance(self,relation_list,
                                        start_object_subset=None):
        # Compute stochastic matrix for the path
        matrix = self.GetPathStochasticMatrix(relation_list)
        # Get size of the start object group
        start_og = self.object_group_dic[self.GetLinkGroup(relation_list[0]).start_id]
        # If no subset is given, there is a fast way
        if start_object_subset==None:
            P=np.ones(start_og.size)
            P=P/P.sum()
            P=np.append(P,[0]) # This zero is the probability of starting at the sink of the group
        else: # else, we have to assemble the array p
            # TODO: check that it is a proper subset
            P=np.zeros(start_og.size+1) # The last position is for the sink of the group
            positions = [start_og.objects_ids_queue.index(start_og.objects_ids[name]) for name in start_object_subset]
            P[positions] = 1
            P=P/P.sum()
        return matrix.T.dot(P);

    def GetSetCollectiveTrueDiversity(self,relation_list,alpha,
                                    start_object_subset=None,
                                    renormalize=True):
        P=self.GetPathProportionalAbundance(relation_list,start_object_subset=start_object_subset)
        # Move mass from the sink node to the rest of the nodes
        if renormalize:
            P=P[:-1]
            if P.sum()<1e-8:
                raise ValueError('Proportional Abundance cannot be renormalized because all mass was in the sink.')
            P=P/P.sum()
        return TrueDiversity(P,alpha);

    def GetSetMeanIndTrueDiversity(self,relation_list,alpha,
                                method='geo',
                                start_object_subset=None):
        if method not in ['wpm','ar','geo']:
            raise ValueError('Invalid mean method. Admitted methods are wpm (weighted power mean), ar (arithmetic), or geo (geometric).')
        # Compute stochastic matrix for the path
        matrix = self.GetPathStochasticMatrix(relation_list).tolil()
        # Deleting proportional abundance of the sink start object
        PAs=matrix.data[:-1]
        # Selecting the propostional abundaces of the start object subset
        if start_object_subset is not None:
            positions = [start_og.objects_ids_queue.index(start_og.objects_ids[name]) for name in start_object_subset]
            PAs=PAs[PAs]
        # computing the diversity of each proportional abundance
        diversities=[]
        for P in PAs:
            diversities.append(TrueDiversity(P,alpha))
        diversities=np.array(diversities)
        # Computing the mean
        if method=='ar':
            return diversities.mean()
        elif method=='geo':
            return diversities.prod()**(1.0/diversities.size)
        elif method=='wpm':
            raise ValueError('Weighted Power Mean Method not implemented yet.')
