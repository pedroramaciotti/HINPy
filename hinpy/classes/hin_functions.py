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

    # dropping duplicates
    n_rows = table.shape[0]
    table.drop_duplicates(inplace=True)
    if n_rows != table.shape[0]:
        print('WARNING: Dataset had duplicated lines that were eliminated.')

    # Things to check (TODO)
    # - Conformity: that link groups (relations) have all links starting and ending in the same groups of objects
    # - No multi-link inside a link group (relation)

    return table;

def CheckPath(relation_list):

    # Checking that object is list
    if not isinstance(relation_list, list):
        raise TypeError('Argument is not a list.')
    # Checking that elements of list are names
    for e in relation_list:
        if not type(e) == str:
            raise TypeError('An element of the path list are not string.')
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




