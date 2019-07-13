#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 13:53:53 2019

@author: pedro
"""

import hinpy
import pandas as pd
import numpy as np

pd.set_option('mode.chained_assignment', 'raise')

hin = hinpy.classes.HIN(name='ml20m',filename='../../DataBases/MovieLens/ml-20m/movielens20M_hin.csv',verbose=True)