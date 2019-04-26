import pandas as pd
import numpy as np

from .link_group_class import LinkGroup
from .object_group_class import ObjectGroup

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
            # Checkingtable.fillna('',inplace=True)
            table['relation']     =table['relation'].astype(str)
            table['start_group']  =table['start_group'].astype(str)
            table['start_object'] =table['start_object'].astype(str)
            table['start_group']  =table['start_group'].astype(str)
            table['start_object'] =table['start_object'].astype(str)
            table['end_group']    =table['end_group'].astype(str)
            table['end_object']   =table['end_object'].astype(str)
            table['timestamp']    =table['timestamp'].astype(str).apply(lambda x: pd.Timestamp(x))

        # Things to check (TODO)
        # - Conformity: that link groups (relations) have all links starting and ending in the same groups of objects
        # - No multi-link inside a link group (relation)

        # Filling the fields of
        self.table = table
        self.name = name

        self.object_group_dic = {}
        self.link_group_dic   = {}

        # Creating Object Groups
        object_group_id = 0
        for og_name in list(set(table.start_group.unique())|set(table.end_group.unique())):
            o_list =list(table[table.start_group==og_name].start_object)
            o_list+=list(table[table.end_group==og_name].end_object)
            o_list=list(set(o_list))
            self.object_group_dic[object_group_id] = ObjectGroup(object_list=o_list,
                                                                name=og_name,
                                                                id=object_group_id)
            object_group_id+=1

        # Creating Link Groups
        link_group_id=0
        for lg_name in table.relation.unique():
            sog_name = table[table.relation==lg_name].start_group.iloc[0]
            eog_name   = table[table.relation==lg_name].end_group.iloc[0]
            self.link_group_dic[link_group_id] = LinkGroup(table=table[table.relation==lg_name],
                                                            name=lg_name,
                                                            id=link_group_id,
                                                            start_og=self.GetObjectGroup(sog_name),
                                                            end_og=self.GetObjectGroup(eog_name))
            link_group_id+=1

        return;

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
                return og;
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
