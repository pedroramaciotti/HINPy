import pandas as pd
import numpy as np

from hinpy.classes.hin_class import *

from hinpy.rs.pure_popularity import *
from hinpy.rs.content_based import *
from hinpy.rs.surprise_based import *
from hinpy.rs.random_rs import *

def HINRS(hin,relation_name,parameters,verbose=False):
    """
    Compute prediction values for links in the Link Group used to produce
    the recommendations. Predicted values are ratings of number of consumptions
    depending on the context: explicit or implicit recommendation.

    Parameters
    ----------
    table : DataFrame
        DataFrame containing the information of the bipartite graph
        representing implicit or explicit user consumption information.
    parameters : dic
        Dictionary with the information establishing the different parameters
        of the recommendation methods.
    hin : HIN
        The HIN object that will be used to compute the recommendation if
        needed.
    """

    # Check that parameters has a 'method'key
    if 'method' not in [k for k,v in parameters.items()]:
        raise ValueError('No method specified in parameters.')

    # Applyting the chosen RS
    print(parameters['method'])
    if parameters['method']=='Copy':
        print('Copy')
        predicted_table = table.copy(deep=True)
        predicted_table.loc[:,'relation']='copied_%s'%table.relation.iloc[0]
        report_dic = {}
    # Explicit- SURPRISE-based RS
    elif parameters['method'] in ['UBCF','Z-UBCF','IBCF','SVD','NMF','CClustering']:

        table = hin.table[hin.table.relation==relation_name].copy(deep=True)
        predicted_table,report_dic = SurpriseBased(table,relation_name,parameters,verbose=verbose)
    # Content-based
    elif parameters['method']=='CB':

        like_table = hin.table[hin.table.relation==relation_name]
        seen_table = hin.table[hin.table.relation==parameters['seen_relation']]
        # Getting the ponderation of path stochastic matrices
        for p in range(len(parameters['paths'])):
            if p==0:
                matrix = parameters['paths_weights'][p]*hin.GetPathStochasticMatrix(parameters['paths'][p])[:-1,:-1]
            else:
                matrix = matrix + parameters['paths_weights'][p]*hin.GetPathStochasticMatrix(parameters['paths'][p])[:-1,:-1]
        matrix = matrix.tolil()
        seen_matrix = hin.GetLinkGroup(parameters['seen_relation']).stochastic_matrix.tolil()
        # Getting start and end object group position dictionaries
        end_objects_dic = hin.GetLinkGroupEndObjectGroup(relation_name).OjectNameDicFromPosition()
        start_objects_dic = hin.GetLinkGroupStartObjectGroup(relation_name).OjectNameDicFromPosition()
        # Producing the recommendations
        predicted_table,report_dic = ContentBased(matrix,seen_matrix,like_table,start_objects_dic,end_objects_dic,parameters,verbose=verbose)
    # Pure Popularity
    elif parameters['method']=='EPP':
        predicted_table,report_dic = ExplicitPurePopularity()
    elif parameters['method']=='IPP':
        like_table = hin.table[hin.table.relation==relation_name]
        seen_table = hin.table[hin.table.relation==parameters['seen_relation']]
        start_objects = hin.GetLinkGroupStartObjectGroup(relation_name).GetNames()
        predicted_table,report_dic = ImplicitPurePopularity(like_table,seen_table,start_objects,parameters,verbose=verbose)
    # Random
    elif parameters['method']=='random':
        predicted_table,report_dic = RandomRecommender(start_object_group=hin.GetLinkGroupStartObjectGroup(relation_name),
                                                       end_object_group=hin.GetLinkGroupEndObjectGroup(relation_name),
                                                       parameters=parameters,verbose=verbose)
    else:
        raise ValueError('Unrecognized RS method named %s'%parameters['method'])


    return predicted_table,report_dic;
