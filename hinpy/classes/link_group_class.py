import pandas as pd
from scipy import sparse
import numpy as np

from time import time as TCounter

from hinpy.general import *
from .link_group_functions import *

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


    def __init__(self, table, name, id, start_og, end_og,compute_stochastic_matrix=True,
                verbose=False):
        """
        LinkTypeClass

        Parameters:
        -----------
        name : str
            Name of the group of links (relation).
        id : int
            Global id of the group of links.
        start_og : ObjectGroup Class

        end_og : ObjectGroup Class

        table : pd.DataFram
        """
        t=TCounter()
        VerboseMessage(verbose,'Building Link Group %s...'%name)
        self.name = name
        self.info = {}
        self.id   = id
        self.start_id  = start_og.id
        self.end_id    = end_og.id
        self.size = table.shape[0]
        if compute_stochastic_matrix:
            self.stochastic_matrix = StochasticMatrix(table, start_og, end_og,verbose=verbose)
        else:
            self.stochastic_matrix = None
        VerboseMessage(verbose,'Link Group %s built in %s.'%(name,ETSec2ETTime(TCounter()-t)))
        return;

    
