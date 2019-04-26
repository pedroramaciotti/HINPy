

import hinpy

import pandas as pd
import numpy as np



a,b=hinpy.datasets.random_hin_generator([('user',10),('item',10)],[])

hin = hinpy.classes.HIN(name='hola',filename='datasets/douban_movie_hin.csv')

#for k,v in hin.object_group_dic.items():
#    print('\n')
#    print('object id %d : %s. Size=%d'%(k,v.name,v.size))
#    print(v.objects_names)
#    print(v.objects_ids)
#    print(v.objects_ids_queue)