import pandas as pd
import numpy as np


from hinpy.classes.object_group_class import *
from time import time as TCounter


def RandomRecommender(start_object_group,end_object_group,parameters,verbose=False):



    start_objects = start_object_group.GetNames()
    end_objects = end_object_group.GetNames()

    start_group = start_object_group.name
    end_group = end_object_group.name

    relation_name=''
    timestamp=pd.Timestamp('')

    if verbose:
        t=TCounter()
        VerboseMessage(verbose,'Computing Random Recommendations of %s for %s...'%(end_group,start_group))

    recommended_table=pd.DataFrame(columns=['relation','start_group', 'start_object', 'end_group', 'end_object',
            'value','timestamp'])

    # For each start object...
    counter=0
    for start_obj in start_objects:
        # We select random topK_predictions objects to recommend
        user_list = np.random.choice(end_objects,size=parameters['topK_predictions'])
        for end_obj in user_list:
            recommended_table.loc[counter] = [relation_name,start_group,start_obj,end_group,end_obj,'',timestamp]
            counter+=1

    if verbose:
        VerboseMessage(verbose,'Random Recommendations computed in %s.'%(ETSec2ETTime(TCounter()-t)))

    return recommended_table,{};
