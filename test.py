

import hinpy
import pandas as pd
import numpy as np

a,b=hinpy.datasets.random_hin_generator([('user',10),('item',10)],[])

hin = hinpy.classes.HIN(name='hola',filename='datasets/example1.csv')

p=hin.GetPathProportionalAbundance(['rates','is_of_type'])


def likes(x):
    if x<5:
        return False;
    else:
        return True;

hin.CreateLinkGroupFromLinkGroup('rates','likes',likes)




hin.MergeLinkGroups('is_of_type','is_of_type2','new_is_of_type')

a=hin.GetLinkGroup('new_is_of_type').stochastic_matrix.toarray()

hin.DeleteLinkGroup('likes')

['id: %d, name: %s'%(k,lg.name) for k,lg in hin.link_group_dic.items()]