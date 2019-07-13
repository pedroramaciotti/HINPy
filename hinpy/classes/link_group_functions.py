import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.preprocessing import normalize

from time import time as TCounter

from hinpy.general import *

from .object_group_class import ObjectGroup


def StochasticMatrix(table, start_og, end_og):
    # Directed matrices
    matrix = sparse.lil_matrix((start_og.size,end_og.size))
    for row in table.itertuples():
        matrix[start_og.GetObjectQueuePos(row.start_object),end_og.GetObjectQueuePos(row.end_object)]=1.0
    matrix = sparse.vstack([matrix,sparse.lil_matrix((1,end_og.size))])
    matrix = sparse.hstack([matrix,sparse.lil_matrix((start_og.size+1,1))])
    matrix = matrix.tolil()
    # Connecting sink nodes
    matrix[start_og.size,end_og.size]=1.0
    # Detecting unconnected objects and connecting them to sinks
    unconnected_objects=np.setdiff1d(start_og.GetNames(),table.start_object.unique())
    for object_name in unconnected_objects:
        matrix[start_og.GetObjectQueuePos(object_name),-1]=1.0
    # Normalizing rows
    return normalize(sparse.csr_matrix(matrix),norm='l1',axis=1)
