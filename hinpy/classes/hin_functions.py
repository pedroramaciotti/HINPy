import pandas as pd

def CheckTable(table):

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

    return table;

def CheckPath(relation_list):

    # TODO: Check conformity of the path

    return relation_list;

###########################################
# Extract from tables                     #
###########################################

def GetObjectListFromTable(table):
    o_list =list(table.start_object)
    o_list+=list(table.end_object)
    o_list =list(set(o_list))
    return o_list;

def GetObjectsFromTableWithGroup(table,object_group_name):
    o_list =list(table[table.start_group==object_group_name].start_object)
    o_list+=list(table[table.end_group==object_group_name].end_object)
    o_list=list(set(o_list))
    return o_list;
