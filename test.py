

import hinpy

import pandas as pd
import numpy as np



a,b=hinpy.datasets.random_hin_generator([('user',10),('item',10)],[])

hin = hinpy.classes.HIN(name='hola',filename='datasets/example1.csv')

p=hin.GetPathProportionalAbundance(['rates','is_of_type'])

d=hin.GetSetCollectiveTrueDiversity(['rates','is_of_type'],1)
#m1=hin.GetLinkGroup('rates').stochastic_matrix.toarray()
m2=hin.GetPathStochasticMatrix(['rates','is_of_type']).toarray()
a=hin.GetSetMeanIndTrueDiversity(['rates','is_of_type'],1)

#m3=hin.GetLinkGroup('rates').stochastic_matrix.toarray()
#
#matrix=hin.GetLinkGroup('is_of_type').stochastic_matrix
#
#p=np.ones(3)
#p=p/p.sum()
#p=np.append(p,[0])
#
#
#g=hin.GetObjectGroup('user')