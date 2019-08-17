import pandas as pd
import numpy as np

from time import time as TCounter

from hinpy.general import *


def ContentBased(matrix,seen_matrix,likes_table,start_objects_dic,end_objects_dic,parameters,verbose=False):

    if verbose:
        t=TCounter()
        VerboseMessage(verbose,'Computing Content-Based Filtering of %s...'%(likes_table.relation.iloc[0]))

    # Retrieving names
    relation_name = likes_table.relation.iloc[0]
    start_group = likes_table.start_group.iloc[0]
    end_group = likes_table.end_group.iloc[0]
    timestamp = pd.Timestamp('')

    # Producing the actual recommendations
    ######################################

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
        ordered_cols = ordered_cols[:parameters['topK_predictions']]
        # Get start object
        start_obj = start_objects_dic[row_id]
        for pos in ordered_cols:
            end_objects_dic
            recommended_table.loc[counter]=[relation_name,start_group,start_obj,end_group,end_objects_dic[pos],'',timestamp]
            counter+=1
    if verbose:
        VerboseMessage(verbose,'Content-Based Filtering computed in %s.'%(ETSec2ETTime(TCounter()-t)))
    return recommended_table,{};
