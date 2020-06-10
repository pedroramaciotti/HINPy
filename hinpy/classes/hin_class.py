import pandas as pd
import numpy as np
import collections

from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats.mstats import gmean
from sklearn.preprocessing import normalize


from time import time as TCounter

from .link_group_class import LinkGroup
from .object_group_class import ObjectGroup
from .hin_functions import *
from hinpy.rs.hin_rs import *
from hinpy.diversity.truediversity import *
from hinpy.diversity.other_measures import *
from hinpy.general import *
from .hin_graphics import *


class HIN:
    """
    HIN: Heterogeneous Information Network Object

    """

    def __init__(self,filename=None,table=None,name=None,inverse_relations=True,
                 verbose=False):

        # If there is no table, create from file
        if table is None:
            if filename is None:
                raise ValueError('HIN object has to be created from a table or from a file.')
            columns=['relation',
                    'start_group','start_object',
                    'end_group','end_object',
                    'value','timestamp']
            t=TCounter()
            VerboseMessage(verbose,'Reading table from %s ...'%filename)
            table=pd.read_csv(filename,sep=',',header=None,names=columns,low_memory=False)
            VerboseMessage(verbose,'Table read in %s.'%ETSec2ETTime(TCounter()-t))
        # Cheking the table
        t=TCounter()
        table = CheckTable(table)
        VerboseMessage(verbose,'Table checked in %s.'%ETSec2ETTime(TCounter()-t))

        # TODO: Aggregation of multi edges: None, Average, Sum

        # Filling the fields
        self.table = table
        self.name = name
        self.info = {}

        # Building Object and Link Groups from Table
        t=TCounter()
        self.ReBuildObjectGroupsFromTable(verbose)
        VerboseMessage(verbose,'Object Groups built in %s.'%ETSec2ETTime(TCounter()-t))
        t=TCounter()
        self.ReBuildLinkGroupsFromTable(verbose)
        VerboseMessage(verbose,'Link Groups built in %s.'%ETSec2ETTime(TCounter()-t))

        if inverse_relations:
            for relation_name in self.table.relation.unique():
                self.CreateInverseLinkGroup(relation_name,verbose=verbose)

        return;

    ###########################################
    # Functions Changing Link Groups          #
    ###########################################

    # New ones !

    def CreateLinkGroup(self,linkgroup,name,
                        datetimes=None,
                        condition=None,
                        verbose=False):
        if (datetimes!=None and condition!=None) or (datetimes==None and condition==None):
            raise ValueError('To create a link group you have to provide datetime bounds or (XOR) a condition method.')
        
        if datetimes!=None:
            # Get the group ids of the Link Group
            og_start = self.object_group_dic[self.GetLinkGroup(linkgroup).start_id]
            og_end  = self.object_group_dic[self.GetLinkGroup(linkgroup).end_id]
            # Getting subtable of the Link Group
            subtable=self.table[self.table.relation==linkgroup].copy(deep=True)
            # Applyting the condition
            subtable=subtable[(subtable.timestamp>=pd.Timestamp(datetimes['min']))&(subtable.timestamp<=pd.Timestamp(datetimes['max']))]
            # Changing name
            subtable.loc[:,'relation'] = name
            # Saving the new Link Group
            self.table = self.table.append(subtable).reset_index(drop=True)
            lg_id = self.GetNewLinkGroupID()
            self.link_group_dic[lg_id] = LinkGroup(table=subtable,
                                                    name=subtable.relation.iloc[0],
                                                    id=lg_id,
                                                    start_og=og_start,
                                                    end_og=og_end,
                                                    verbose=verbose)
            return;
        if condition!=None:
            raise ValueError('Link group creation with ')


    # TODO: re-organize and move to link_group_functions

    def CreateInverseLinkGroup(self,existing_relation_name,new_relation_name=None,verbose=False):
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
        new_subtable.timestamp=subtable.timestamp
        new_subtable.value=subtable.value
        # Giving a name to the new relation
        if new_relation_name is None:
            new_subtable.relation='inverse_'+existing_relation_name
        else:
            new_subtable.relation=new_relation_name
        # Appending the table and changing the HIN
        self.table=self.table.append(new_subtable).reset_index(drop=True)
        new_link_group_id = self.GetNewLinkGroupID()
        sog_name=new_subtable.start_group.iloc[0]
        eog_name=new_subtable.end_group.iloc[0]
        self.link_group_dic[new_link_group_id] = LinkGroup(table=new_subtable,
                                                        name=new_subtable.relation.iloc[0],
                                                        id=new_link_group_id,
                                                        start_og=self.GetObjectGroup(sog_name),
                                                        end_og=self.GetObjectGroup(eog_name),
                                                        verbose=verbose)
    def CreateSubsampledLinkGroup(self,relation_name,new_relation_name,fraction,
                                    per_start_object=True,verbose=False):
        # Get the group ids of the Link Group
        og_start = self.object_group_dic[self.GetLinkGroup(relation_name).start_id]
        og_end  = self.object_group_dic[self.GetLinkGroup(relation_name).end_id]
        # Getting subtable of the Link Group
        subtable=self.table[self.table.relation==relation_name].copy(deep=True)
        # Subsampling
        if per_start_object:
            grouped = subtable.groupby('start_object')
            subtable = grouped.apply(lambda x: x.sample(frac=fraction))
        else:
            subtable=subtable.sample(frac=fraction)
        # Changing name
        subtable.loc[:,'relation'] = new_relation_name
        # Saving the new Link Group
        self.table = self.table.append(subtable).reset_index(drop=True)
        lg_id = self.GetNewLinkGroupID()
        self.link_group_dic[lg_id] = LinkGroup(table=subtable,
                                                name=subtable.relation.iloc[0],
                                                id=lg_id,
                                                start_og=og_start,
                                                end_og=og_end,
                                                verbose=verbose)
        return;

    def DeleteLinkGroup(self,relation_name):
        self.link_group_dic.pop(self.GetLinkGroupId(relation_name))
        self.table=self.table[self.table.relation!=relation_name].reset_index(drop=True)
        return;

    def MergeLinkGroups(self,relation_name, relation_name_to_merge,
                        new_relation_name=None, delete_merged_relation=False,
                        verbose=False):
        """
        Merge contents of relation_name_to_merge table into relation_name table.

        """
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
        self.table=self.table.append(merged_table).reset_index(drop=True)
        lg_id = self.GetLinkGroupId(relation_name)
        self.link_group_dic[lg_id] = LinkGroup(table=merged_table,
                                                name=merged_table.relation.iloc[0],
                                                id=lg_id,
                                                start_og=og1_start,
                                                end_og=og1_end,
                                                verbose=verbose)
        if delete_merged_relation:
            self.DeleteLinkGroup(relation_name_to_merge)
        return;

    def CreateLinkGroupFromLinkGroup(self,relation_name,new_relation_name,condition_method,
                                    verbose=False):
        # Get the group ids of the Link Group
        og_start = self.object_group_dic[self.GetLinkGroup(relation_name).start_id]
        og_end  = self.object_group_dic[self.GetLinkGroup(relation_name).end_id]
        # Getting subtable of the Link Group
        subtable=self.table[self.table.relation==relation_name].copy(deep=True)
        # Applyting the condition
        subtable=subtable[subtable.value.apply(condition_method)]
        # Changing name
        subtable.loc[:,'relation'] = new_relation_name
        # Saving the new Link Group
        self.table = self.table.append(subtable).reset_index(drop=True)
        lg_id = self.GetNewLinkGroupID()
        self.link_group_dic[lg_id] = LinkGroup(table=subtable,
                                                name=subtable.relation.iloc[0],
                                                id=lg_id,
                                                start_og=og_start,
                                                end_og=og_end,
                                                verbose=verbose)
        return;

    def CreateLinkGroupFromLinkGroupWithDates(self,relation_name,new_relation_name,limit_dates,
                                    verbose=False):
        # Get the group ids of the Link Group
        og_start = self.object_group_dic[self.GetLinkGroup(relation_name).start_id]
        og_end  = self.object_group_dic[self.GetLinkGroup(relation_name).end_id]
        # Getting subtable of the Link Group
        subtable=self.table[self.table.relation==relation_name].copy(deep=True)
        # Applyting the condition
        subtable=subtable[(subtable.timestamp>=pd.Timestamp(limit_dates['min']))&(subtable.timestamp<=pd.Timestamp(limit_dates['max']))]
        # Changing name
        subtable.loc[:,'relation'] = new_relation_name
        # Saving the new Link Group
        self.table = self.table.append(subtable).reset_index(drop=True)
        lg_id = self.GetNewLinkGroupID()
        self.link_group_dic[lg_id] = LinkGroup(table=subtable,
                                                name=subtable.relation.iloc[0],
                                                id=lg_id,
                                                start_og=og_start,
                                                end_og=og_end,
                                                verbose=verbose)
        return;

    def CreateLinkGroupFromTable(self,new_table,new_relation_name=None,verbose=False):
        # Check table for start/end group uniqueness and existence, check consistent relation name
        if new_table.start_group.unique().size!=1 or new_table.end_group.unique().size!=1:
            raise ValueError('Table has links between more than two object groups.')
        # Get the group ids of the Link Group
        og_start_name = new_table.start_group.iloc[0]
        og_end_name = new_table.end_group.iloc[0]
        og_start = self.GetObjectGroup(og_start_name)
        og_end = self.GetObjectGroup(og_end_name)
        subtable = new_table.copy(deep=True)
        if new_relation_name is None:
            relation_name = new_table.loc[:,'relation'].iloc[0]
        else:
            relation_name = new_relation_name
            subtable.loc[:,'relation'] = new_relation_name
        # Saving the new Link Group
        self.table = self.table.append(subtable).reset_index(drop=True)
        lg_id = self.GetNewLinkGroupID()
        self.link_group_dic[lg_id] = LinkGroup(table=subtable,
                                                name=relation_name,
                                                id=lg_id,
                                                start_og=og_start,
                                                end_og=og_end,
                                                verbose=verbose)
        return;

    def CreateLinkGroupFromConfigurationModel(self,relation_name,new_relation_name,
                                    verbose=False):
        # Get the group ids of the Link Group
        og_start = self.object_group_dic[self.GetLinkGroup(relation_name).start_id]
        og_end  = self.object_group_dic[self.GetLinkGroup(relation_name).end_id]
        # Getting subtable of the Link Group
        subtable=self.table[self.table.relation==relation_name].copy(deep=True)
        # Shuffling end objects
        subtable.loc[:,'end_object'] = subtable.loc[:,'end_object'].sample(frac=1).values
        # Changing name
        subtable.loc[:,'relation'] = new_relation_name
        # Saving the new Link Group
        self.table = self.table.append(subtable).reset_index(drop=True)
        lg_id = self.GetNewLinkGroupID()
        self.link_group_dic[lg_id] = LinkGroup(table=subtable,
                                                name=subtable.relation.iloc[0],
                                                id=lg_id,
                                                start_og=og_start,
                                                end_og=og_end,
                                                verbose=verbose)
        return;

    def CreateLinkGroupFromRS(self,relation_name,new_relation_name,parameters,
                                        verbose=False):

        """

        """
        # Creating the recommendation table
        predicted_table,report = HINRS(self,relation_name,parameters=parameters,verbose=verbose)
        predicted_table.loc[:,'relation']= new_relation_name
        # Creating the new Link Group from the recommendation
        self.table = self.table.append(predicted_table).reset_index(drop=True)
        new_link_group_id = self.GetNewLinkGroupID()
        lg = self.GetLinkGroup(relation_name)
        og_start = self.GetLinkGroupStartObjectGroup(lg.name)
        og_end   = self.GetLinkGroupEndObjectGroup(lg.name)
        self.link_group_dic[new_link_group_id] = LinkGroup(table=predicted_table,
                                                name=new_relation_name,
                                                id=new_link_group_id,
                                                start_og=og_start,
                                                end_og=og_end,
                                                verbose=verbose)
        self.link_group_dic[new_link_group_id].info = report

        return;

    ###########################################
    # Build Object and Link Groups from Table #
    ###########################################

    def ReBuildObjectGroupsFromTable(self,verbose=False):
        self.object_group_dic = {}
        object_group_id = 0
        for og_name in list(set(self.table.start_group.unique())|set(self.table.end_group.unique())):
            o_list = GetObjectsFromTableWithGroup(self.table,og_name)
            self.object_group_dic[object_group_id] = ObjectGroup(object_list=o_list,
                                                                name=og_name,
                                                                id=object_group_id,
                                                                verbose=verbose)
            object_group_id+=1
        return;

    def ReBuildLinkGroupsFromTable(self,verbose=False):
        self.link_group_dic   = {}
        link_group_id=0
        for lg_name in self.table.relation.unique():
            sog_name = self.table[self.table.relation==lg_name].start_group.iloc[0]
            eog_name = self.table[self.table.relation==lg_name].end_group.iloc[0]
            self.link_group_dic[link_group_id] = LinkGroup(table=self.table[self.table.relation==lg_name],
                                                            name=lg_name,
                                                            id=link_group_id,
                                                            start_og=self.GetObjectGroup(sog_name),
                                                            end_og=self.GetObjectGroup(eog_name),
                                                            verbose=verbose)
            link_group_id+=1
        return


    #####################################
    # HIN and Group Property Retrievers #
    #####################################

    # TODO: re-organize and move to hin_functions

    # Get ObjectGroup from name
    def GetObjectGroup(self,name):
        for og_id,og in self.object_group_dic.items():
            if og.name==name:
                return og;
        raise ValueError('Object Group %s not found'%name)
    # Get ObjectGroup at start of LinkGroup from name
    def GetLinkGroupStartObjectGroup(self,name):
        return self.GetObjectGroup(self.object_group_dic[self.GetLinkGroup(name).start_id].name)
    # Get ObjectGroup at end of LinkGroup from name
    def GetLinkGroupEndObjectGroup(self,name):
        return self.GetObjectGroup(self.object_group_dic[self.GetLinkGroup(name).end_id].name)
    # Get LinkGroup from name
    def GetLinkGroup(self,name):
        for lg_id,lg in self.link_group_dic.items():
            if lg.name==name:
                return lg;
        raise ValueError('Link Group %s not found'%name)
    # Get LinkGroup density from name
    def GetLinkGroupDensity(self,name):
        sogs = self.GetLinkGroupStartObjectGroup(name).size
        eogs = self.GetLinkGroupEndObjectGroup(name).size
        lgs =  self.GetLinkGroup(name).size
        return lgs/(sogs*eogs);

    # Get Ids of ObjectGroup from name
    def GetObjectGroupId(self,name):
        for og_id,og in self.object_group_dic.items():
            if og.name==name:
                return og_id;
        raise ValueError('Object Group %s not found'%name)
    # Get Ids of LinkGroup from name
    def GetLinkGroupId(self,name):
        for lg_id,lg in self.link_group_dic.items():
            if lg.name==name:
                return lg_id;
        raise ValueError('Link Group %s not found'%name)

    # Get names of ObjectGroups
    def GetObjectGroupsNames(self):
        return [og.name for og_id,og in self.object_group_dic.items()]

    # Get names of LinkGroups
    def GetLinkGroupsNames(self):
        return [lg.name for lg_id,lg in self.link_group_dic.items()]

    # Get 
    def GetObjectGroupPositionDic(self,name):
        return self.GetObjectGroup(name).OjectPositionDicFromName();
    #
    def GetObjectGroupObjectDic(self,name):
        return self.GetObjectGroup(name).OjectNameDicFromPosition();

    # Get vacant id for new groups
    def GetNewLinkGroupID(self):
        return FirstAbsentNumberInList([k for k,v in self.link_group_dic.items()])

    def GetNewObjectGroupID(self):
        return FirstAbsentNumberInList([k for k,v in self.object_group_dic.items()])


    # Get path-related objects

    def GetPathStartGroupPositionDic(self,path):
        return self.GetLinkGroupStartObjectGroup(path[0]).OjectPositionDicFromName();
    def GetPathEndGroupPositionDic(self,path):
        return self.GetLinkGroupEndObjectGroup(path[-1]).OjectPositionDicFromName();


    ##############################################
    # Path Proportional Abundances & Diversities #
    ##############################################

    def stochastic_matrix(self,path):
        path=CheckPath(path)
        matrix=self.GetLinkGroup(path[0]).stochastic_matrix
        for relation in path[1:]:
            matrix=matrix*self.GetLinkGroup(relation).stochastic_matrix
        return matrix;

    def proportional_abundance(self,path,initial_p=None,include_sink=False):
        path=CheckPath(path)
        # Compute stochastic matrix for the path
        matrix = self.stochastic_matrix(path)
        # Get size of the start object group
        start_og = self.object_group_dic[self.GetLinkGroup(path[0]).start_id]
        if initial_p is not None:
            p=initial_p
        else:
            p=np.ones(start_og.size)
        p=p/p.sum()
        p=np.append(p,[0]) #<- probability of starting at sink = 0
        pa = matrix.T.dot(p)
        if include_sink:
            return pa;
        else:
            return pa[:-1]/pa[:-1].sum();

    def proportional_abundances(self,path,include_sink=False):
        path=CheckPath(path)
        matrix=self.stochastic_matrix(path)
        if include_sink:
            return matrix;
        else:
            matrix=matrix[:-1,:-1]
            return normalize(matrix,norm='l1',axis=1);#<- if all mass went to sink pa=0

    def individual_diversities(self,path,alpha=1.0,include_sink=False):
        path=CheckPath(path)
        pas = self.proportional_abundances(path,include_sink=include_sink).tolil().data
        diversities=[]
        for p in pas:
            if np.abs(np.sum(p)-1.0)<1e-4:
                diversities.append(TrueDiversity(p,alpha))
            else:
                diversities.append(np.nan)
        return np.array(diversities);

    def mean_diversity(self,path,alpha=1.0,include_sink=False,method='arithmetic'):
        path=CheckPath(path)
        diversities = self.individual_diversities(path,alpha=alpha,include_sink=include_sink)
        # Computing the mean
        if method=='arithmetic':
            return diversities.mean()
        elif method=='geo':
            return gmean(diversities)
        elif method=='wpm':
            raise ValueError('Weighted Power Mean Method not implemented yet.')

    def collective_diversity(self,path,alpha=1.0,include_sink=False):
        path=CheckPath(path)
        p=self.proportional_abundance(path,include_sink=include_sink)
        if np.abs(p.sum()-0.0)<1e-6:
            raise ValueError('All mass was in the sink.')
        return TrueDiversity(p,alpha);

    ##############################################
    # Value propagation                          #
    ##############################################

    def path_value_aggregation(self,values_dic,path):
        """
        Aggregate values using a meta-path. Values in the ending
        object group are aggregated into values for the starting 
        object group.
        """
        path=CheckPath(path)
        # Setting the ending object group position
        eg_pos_dic = self.GetPathEndGroupPositionDic(path)
        eg = self.GetLinkGroupEndObjectGroup(path[-1])
        # Checking that values conforms ending obj. group
        # (length: dictionary has the same num. of elements)
        # if eg.size!=len(values_dic):
        #     raise ValueError
        # (inclusion: all keys are objects of the group)
        values_dic_keys = [k for k,v in values_dic.items()]
        if np.setdiff1d(eg.object_list,values_dic_keys).size>0:
            raise ValueError('Values must be provided for all objects in %s.'%eg.name)
        # Inverse ending object group position dictionaries
        inv_eg_pos_dic = dict((v, k) for k, v in eg_pos_dic.items())
        # Put values from values_dic in a vector in order given by eg_pos_dic
        
        e_values_vec = np.array([values_dic[inv_eg_pos_dic[i]] for i in range(eg.size)])
        # proportional abundances matrix is (starting obj. group size)x(ending obj. group size)
        PAM = self.proportional_abundances(path)
        s_values_vec = PAM.dot(e_values_vec)
        s_values_vec[np.ravel(PAM.sum(axis=1))==0.0] = np.nan
        # putting values in a dictionary
        sg_pos_dic = self.GetPathStartGroupPositionDic(path)
        inv_sg_pos_dic = dict((v, k) for k, v in sg_pos_dic.items())
        ordered_s_objects = [v for k,v in collections.OrderedDict(sorted(inv_sg_pos_dic.items())).items() ]
        return dict(zip(ordered_s_objects, s_values_vec));

    #####################################
    # Plotters                          #
    #####################################

    def plot_schema(self,filename=None,
                node_size=700,layout='spring',arrow_size=10,
                edge_labels=True,node_labels=True):
        table = self.table[~self.table.relation.apply(lambda r: r.startswith('inverse_'))].drop_duplicates(subset=['relation','start_group','end_group'])[['start_group','end_group','relation']]
        plot_hin(table,filename=filename,
                node_size=node_size,layout=layout,arrowsize=arrow_size,
                edge_labels=edge_labels,node_labels=node_labels)
        return;







    # THESE ARE LEGACY FUNCTIONS (to be removed)
    #######################################################

    def GetPathStochasticMatrix(self,relation_list):
        path=CheckPath(relation_list)
        matrix=self.GetLinkGroup(path[0]).stochastic_matrix
        for relation in path[1:]:
            matrix=matrix*self.GetLinkGroup(relation).stochastic_matrix
        return matrix;

    def GetPathProportionalAbundance(self,relation_list,
                                        start_object_subset=None,
                                        verbose=False):
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
                                    renormalize=True,
                                    verbose=False):
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
                                start_object_subset=None,
                                verbose=False):
        t=TCounter()

        if method not in ['wpm','ar','geo']:
            raise ValueError('Invalid mean method. Admitted methods are wpm (weighted power mean), ar (arithmetic), or geo (geometric).')
        # Compute stochastic matrix for the path
        matrix = self.GetPathStochasticMatrix(relation_list).tolil()
        # Deleting proportional abundance of the sink start object
        PAs=matrix.data[:-1]
        # Selecting the propostional abundaces of the start object subset
        if start_object_subset is not None:
            positions = [start_og.objects_ids_queue.index(start_og.objects_ids[name]) for name in start_object_subset]
            PAs=PAs[positions]
        # computing the diversity of each proportional abundance
        diversities=[]
        for P in PAs:
            diversities.append(TrueDiversity(P,alpha))
        diversities=np.array(diversities)
        # Computing the mean
        if method=='ar':
            return diversities.mean()
        elif method=='geo':
            return gmean(diversities)
        elif method=='wpm':
            raise ValueError('Weighted Power Mean Method not implemented yet.')

    def GetObjectSetTrueDiversities(self,relation_list,alpha,
                                start_object_subset=None,
                                verbose=False):
        # Compute stochastic matrix for the path
        matrix = self.GetPathStochasticMatrix(relation_list).tolil()
        # Deleting proportional abundance of the sink start object
        PAs=matrix.data[:-1]
        # Selecting the propostional abundaces of the start object subset
        if start_object_subset is not None:
            positions = [start_og.objects_ids_queue.index(start_og.objects_ids[name]) for name in start_object_subset]
            PAs=PAs[positions]
        # computing the diversity of each proportional abundance
        diversities=[]
        for P in PAs:
            diversities.append(TrueDiversity(P,alpha))
        return np.array(diversities);

    ##############################################
    # Classic Diversity Measures for RS          #
    ##############################################

    def SurprisalDivMes(self,relation_name,popularity_relation_name,verbose=False):
        popularity_table = self.table[self.table.relation==popularity_relation_name].copy(deep=True)
        recommended_table = self.table[self.table.relation==relation_name].copy(deep=True)
        return Surprisal(popularity_table,recommended_table,verbose=verbose);

    def NoveltyDivMes(self,relation_name,similarity_relation,verbose=False):
        table = self.table[self.table.relation==relation_name].copy(deep=True)
        sim_matrix = cosine_similarity(self.GetLinkGroup(similarity_relation).stochastic_matrix)
        object_position = self.GetLinkGroupStartObjectGroup(similarity_relation).OjectPositionDicFromName()
        return Novelty(table,sim_matrix,object_position,verbose=verbose);

    def IntraListSimilarityDivMes(self,relation_name,similarity_relation,verbose=False):
        table = self.table[self.table.relation==relation_name].copy(deep=True)
        sim_matrix = cosine_similarity(self.GetLinkGroup(similarity_relation).stochastic_matrix)
        object_position = self.GetLinkGroupStartObjectGroup(similarity_relation).OjectPositionDicFromName()
        return IntraListSimilarity(table,sim_matrix,object_position,verbose=verbose);

    def PersonalisationDivMes(self,relation_name,verbose=False):
        table = self.table[self.table.relation==relation_name].copy(deep=True)
        return Personalisation(table,verbose=verbose);
