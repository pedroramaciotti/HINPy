import pandas as pd
import numpy as np

from time import time as TCounter

from hinpy.general import *

def ImplicitPurePopularity(like_table,seen_table,start_objects,parameters,verbose=False):
    """
    Pure Popularity likes:
    Items with most likes are recommended. This only takes into account how many
    people liked items, and not the scores.
    """
    if verbose:
        t=TCounter()
        VerboseMessage(verbose,'Computing (Implicit) Pure Popularity of %s relative to %s...'%(like_table.relation.iloc[0],seen_table.relation.iloc[0]))
    # Retrieving names
    relation_name = like_table.relation.iloc[0]
    start_group = like_table.start_group.iloc[0]
    end_group = like_table.end_group.iloc[0]
    timestamp = pd.Timestamp('')
    # Retriving counts per object
    objects_count = like_table[['end_object','value']].groupby('end_object').count().sort_values(by='value',ascending=False)
    # Creating the output DataFrame
    recommended_table=pd.DataFrame(columns=['relation','start_group', 'start_object', 'end_group', 'end_object',
            'value','timestamp'])
    # For each start object...
    counter=0
    for start_obj in start_objects:
        # We select best ranking topK end object that he hasn't rated/seen
        user_list = objects_count[~objects_count.index.isin(seen_table[seen_table.start_object==start_obj].end_object)].iloc[:parameters['topK_predictions']]
        for end_obj in user_list.index:
            recommended_table.loc[counter] = [relation_name,start_group,start_obj,end_group,end_obj,'',timestamp]
            counter+=1
    if verbose:
        VerboseMessage(verbose,'Pure Popularity computed in %s.'%(ETSec2ETTime(TCounter()-t)))
    return recommended_table,{};

def ExplicitPurePopularity():
    """
    Pure Popularity based on scores:
    Items with best scores are recommended. This does not take into account
    how many people rated an item.
    """
    return None;
