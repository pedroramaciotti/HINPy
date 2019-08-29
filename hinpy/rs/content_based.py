import pandas as pd
import numpy as np

from time import time as TCounter

from hinpy.classes.hin_class import *

def ContentBased(hin,relation_name,seen_relation,paths,paths_weights,topK,verbose=False):

    likes_table = hin.table[hin.table.relation==relation_name]
    seen_table = hin.table[hin.table.relation==seen_relation]

    if verbose:
        t=TCounter()
        VerboseMessage(verbose,'Computing Content-Based Filtering of %s...'%(likes_table.relation.iloc[0]))

    # Retrieving names
    start_group = likes_table.start_group.iloc[0]
    end_group = likes_table.end_group.iloc[0]
    timestamp = pd.Timestamp('')

    # Producing the actual recommendations
    ######################################

    # Producing the recommendation

    # Getting the ponderation of path stochastic matrices
    for p in range(len(paths)):
        if p==0:
            matrix = paths_weights[p]*hin.GetPathStochasticMatrix(paths[p])[:-1,:-1]
        else:
            matrix = matrix + paths_weights[p]*hin.GetPathStochasticMatrix(paths[p])[:-1,:-1]
    matrix = matrix.tolil()
    seen_matrix = hin.GetLinkGroup(seen_relation).stochastic_matrix.tolil()
    # Getting start and end object group position dictionaries
    end_objects_dic = hin.GetLinkGroupEndObjectGroup(relation_name).OjectNameDicFromPosition()
    start_objects_dic = hin.GetLinkGroupStartObjectGroup(relation_name).OjectNameDicFromPosition()



    # Table to stock recommendations
    recommended_table = pd.DataFrame(columns=['relation','start_group', 'start_object', 'end_group', 'end_object','value','timestamp'])
    counter = 0

    # For each row of the lil matrix
    for row_id in range(matrix.shape[0]):
        # We retrieve the orderer list of columns of elements in decreasing order
        cols = np.array(matrix.rows[row_id])
        ordered_cols = cols[np.argsort(matrix.data[row_id])[::-1]]
        # Get end objects already seen by start object
        seen_columns = seen_matrix.rows[row_id]
        # Delete those already seen by start object
        ordered_cols = ordered_cols[~np.isin(ordered_cols,seen_columns)]
        # Selecting topK end objects
        ordered_cols = ordered_cols[:topK]
        # Get start object
        start_obj = start_objects_dic[row_id]
        for pos in ordered_cols:
            end_objects_dic
            recommended_table.loc[counter]=[relation_name,start_group,start_obj,end_group,end_objects_dic[pos],'',timestamp]
            counter+=1
    if verbose:
        VerboseMessage(verbose,'Content-Based Filtering computed in %s.'%(ETSec2ETTime(TCounter()-t)))
    return recommended_table;
