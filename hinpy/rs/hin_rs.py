import pandas as pd
import numpy as np
from hinpy.rs.pure_popularity import *
from hinpy.rs.content_based import *
from hinpy.rs.surprise_based import *




def HINRS(table,parameters,hin=None):
    """
    Compute recommendations for a HIN and store them in a DataFrame

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

    # Check that the chosen recommendation method exists
    # TODO

    # Applyting the chosen RS

    if parameters['method']=='Copy':
        reco_table = table.copy(deep=True)
        reco_table.loc[:,'relation']=''
        report_dic = {}

    elif parameters['method']=='PurePopularity':
        print('PP')

    else:
        pass


    return reco_table,report_dic;
