import surprise
import pandas as pd
import numpy as np

from time import time as TCounter
from collections import defaultdict

from hinpy.general import *

def SurpriseBased(table,relation_name,parameters,verbose=False):
    """

    """

    report = {}

    # Initial checks
    param_keys=[k for k,v in parameters.items()]
    if ('max_scale' not in param_keys) or ('min_scale' not in param_keys):
        raise ValueError('max_scale and min_scale must be specified in parameters for explicit RS.')
    if 'model_size' not in param_keys:
        raise ValueError('model_size must be specified in parameters for SURPRISE-based RS.')
    if 'topK_predictions' not in param_keys:
        raise ValueError('A size (K) must be given for the recommended list size (topK).')

    # Retrieving names
    start_group = table.start_group.iloc[0]
    end_group = table.end_group.iloc[0]
    timestamp = pd.Timestamp('')

    # Retrieving the table of the bipartite graph in SURPRISE format
    table = table[['start_object','end_object','value']]
    reader = surprise.Reader(rating_scale=(parameters['min_scale'],parameters['max_scale']))
    data = surprise.Dataset.load_from_df(table,reader)

    # Selecting the method from the SURPRISE module
    if parameters['method']=='UBCF':
        method = surprise.KNNBasic(k=parameters['model_size'],verbose=verbose)
    elif parameters['method']=='Z-UBCF':
        method=surprise.KNNWithZScore(k=parameters['model_size'])
    elif parameters['method']=='IBCF':
        method=surprise.KNNBasic(k=parameters['model_size'],sim_options={'user_based':False})
    elif parameters['method']=='SVD':
        method=surprise.SVD(n_factors=parameters['model_size'])
    elif parameters['method']=='NMF':
        method=surprise.NMF(n_factors=parameters['model_size'])
    elif parameters['method']=='CClustering':
        method=surprise.CoClustering(n_cltr_u=parameters['model_size'],n_cltr_i=parameters['model_size'])
    else:
        raise ValueError('Unrecognized SURPRISE-based RS method named %s'%parameters['method'])


    # Computing utility metrics if so specified
    if 'RMSE' in param_keys:
        if parameters['RMSE']:
            results=surprise.model_selection.validation.cross_validate(method,data,measures=['rmse'],cv=5,verbose=verbose)
            rmse = results['test_rmse'].mean()
            report['RMSE']=rmse

    # Training the prediction method
    trainset = data.build_full_trainset()
    del data
    method.fit(trainset)

    # Retrieving unobserved pairs
    t=TCounter()
    VerboseMessage(verbose,'Producing unobserved links...')
    unobserved_links =trainset.build_anti_testset()
    VerboseMessage(verbose,'Unobserved links produced in %s.'%(ETSec2ETTime(TCounter()-t)))

    # Making the predictions
    t=TCounter()
    VerboseMessage(verbose,'Making predictions for unobserved links...')
    predictions = method.test(unobserved_links)
    VerboseMessage(verbose,'Predictions for Unobserved links produced in %s.'%(ETSec2ETTime(TCounter()-t)))

    # Prefiltering predictions with lower scores
    if 'prefilter_score' in param_keys:
        t=TCounter()
        VerboseMessage( verbose,'Prefiltering %d predictions scores lower than %0.1f...'%(len(predictions),parameters['prefilter_threshold']))
        predictions = [p for p in predictions if p[3]>parameters['prefilter_threshold']]
        VerboseMessage(verbose,'Predictions prefiltered in %s, %d remaining.'%(ETSec2ETTime(TCounter()-t),len(predictions)))

    # Selecting only top K predictions
    t=TCounter()
    VerboseMessage( verbose,'Selecting top %d predictions...'%(parameters['topK_predictions']))
    top_recs = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_recs[uid].append((iid, est))
    for uid, user_ratings in top_recs.items():
        user_ratings.sort(key = lambda x: x[1], reverse = True)
        top_recs[uid] = user_ratings[:parameters['topK_predictions']]
    VerboseMessage(verbose,'Predictions selected in %s.'%(ETSec2ETTime(TCounter()-t)))


    # Putting the predictions in a DataFrame
    predictions_table = pd.DataFrame(columns=['relation','start_group', 'start_object', 'end_group', 'end_object',
        'value','timestamp'])
    counter = 0
    t=TCounter()
    VerboseMessage(verbose,'Arranging predictions into a DataFrame table...')
    for k,v in top_recs.items():
        for r in v:
            predictions_table.loc[counter] = [relation_name,start_group,k,end_group,r[0],r[1],timestamp]
            counter += 1

    VerboseMessage(verbose,'Predictions arranged into a table in %s.'%(ETSec2ETTime(TCounter()-t)))

    return predictions_table,report;
