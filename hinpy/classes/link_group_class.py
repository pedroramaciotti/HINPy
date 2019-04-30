import pandas as pd
from .link_group_functions import *
from scipy import sparse
import numpy as np

class LinkGroup():
    """
    LinkTypeClass

    Attributes:
    -----------
    name : str
        Name of the group of links (relation).
    id : int
        Global id of the group of links.
    start_id : int
        Global id of the starting group of objects.
    end_id : int
        Global id of the ending group of objects.
    size : int
        Number of links in the group. Parallel links NOT allowed.
    links_ids_queue : list[int]
        List with the current order of the links' ids.
    table : pd.DataFrame
    """
    def __init__(self, table, name, id, start_og, end_og):
        self.name = name
        self.info = {}
        self.id   = id
        self.start_id  = start_og.id
        self.end_id    = end_og.id
        self.size = table.shape[0]
        self.stochastic_matrix = StochasticMatrix(table, start_og, end_og)

        return;
