import pandas as pd
import numpy as np

from .link_group_class import LinkGroup
from .object_group_class import ObjectGroup
from .hin_functions import *
from hinpy.diversity.truediversity import *

class HIN:
    """HIN: Heterogeneous Information Network Object

    """

    def __init__(self,filename=None,table=None,name=None):

        # If there is no table, create from file
        if table is None:
            if filename is None:
                raise ValueError('HIN object has to be created from a table or from a file.')
            columns=['relation',
                    'start_group','start_object',
                    'end_group','end_object',
                    'value','timestamp']
            table=pd.read_csv(filename,sep=',',header=None,names=columns)

        # Cheking the table
        table = CheckTable(table)

        # TODO: Aggregation of multi edges: None, Average, Sum

        # Filling the fields of
        self.table = table
        self.name = name

        # Building Object and Link Groups from Table
        self.ReBuildObjectGroupsFromTable()
        self.ReBuildLinkGroupsFromTable()

        return;

    ###########################################
    # Build Object and Link Groups from Table #
    ###########################################

    def ReBuildObjectGroupsFromTable(self):
        self.object_group_dic = {}
        object_group_id = 0
        for og_name in list(set(self.table.start_group.unique())|set(self.table.end_group.unique())):
            o_list =list(self.table[self.table.start_group==og_name].start_object)
            o_list+=list(self.table[self.table.end_group==og_name].end_object)
            o_list=list(set(o_list))
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
                                    start_object_subset=None):
        P=self.GetPathProportionalAbundance(relation_list,start_object_subset=start_object_subset)
        # TODO: What to do with mass accumulated on sink?
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
