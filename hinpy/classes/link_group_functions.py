import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.preprocessing import normalize

import copy

from time import time as TCounter
from hinpy.general import *

from .object_group_class import ObjectGroup

def StochasticMatrix(table, start_og, end_og,verbose=False):
    # Edge list with multiplicity
    edgelist = table[['start_object','end_object']].groupby(['start_object','end_object']).size().reset_index().rename(columns={0: 'multiplicity'})
    # Retrieving dictionaries with objects' position as rows and columns
    VerboseMessage(verbose,'dictionaries')
    s_dic = copy.deepcopy(start_og.objects_ids)
    d_dic = copy.deepcopy(end_og.objects_ids)
    # computing row and columns
    edgelist['row'] = edgelist['start_object'].map(s_dic)
    edgelist['col'] = edgelist['end_object'].map(d_dic)
    # Connecting unconnected start objects to sink
    unconnected_object_ids=np.setdiff1d(start_og.objects_ids_queue,edgelist.row.unique())

    # Treating connections to sink nodes

    # Including sink nodes to group row/col dictionaries
    appendable_dic = {'start_object':np.zeros(unconnected_object_ids.size),'end_object':np.zeros(unconnected_object_ids.size),'row':unconnected_object_ids,'col':end_og.size*np.ones(unconnected_object_ids.size),'multiplicity':np.ones(unconnected_object_ids.size)}
    appendable_sink_df = pd.DataFrame(appendable_dic)
    edgelist = edgelist.append(appendable_sink_df, ignore_index=True)
    # linking the two sinks
    edgelist = edgelist.append({'start_object': '','end_object':'','row':start_og.size,'col':end_og.size,'multiplicity':1}, ignore_index=True)
    
    # constructing matrix
    coo = sparse.coo_matrix((edgelist.multiplicity.values,
                      (edgelist.row.values, edgelist.col.values)), shape=(start_og.size+1, end_og.size+1))
    return normalize(sparse.csr_matrix(coo),norm='l1',axis=1);
