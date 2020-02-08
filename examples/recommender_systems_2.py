import hinpy
import pandas as pd
import numpy as np


# CLASSIC RECOMMENDER SYSTEMS AND DIVERSITY METRICS



# Select a dataset

#hin = hinpy.classes.HIN(name='douban movie',filename='datasets/douban_movie_hin.csv',verbose=False,inverse_relations=True)
hin = hinpy.classes.HIN(name='m100k',filename='datasets/movielens100k_hin.csv',verbose=False,inverse_relations=True)
#hin = hinpy.classes.HIN(name='amazon music',filename='datasets/amazon_digital_music_hin.csv',verbose=False,inverse_relations=True)

# use "rates" link group to create the "likes" link group

likes_func = lambda x: True if x>2 else False 
hin.CreateLinkGroupFromLinkGroup('rates','likes',likes)

## Testing classic collaborative filtering:
parameters = {}
parameters['method']='IBCF'# try also UBCF
parameters['min_scale']=1
parameters['max_scale']=5
parameters['model_size']=3
parameters['prefilter_score']=False
parameters['prefilter_threshold']=3.5
parameters['topK_predictions']=4
parameters['RMSE']=True
hin.CreateLinkGroupFromRS('rates','Crecos',parameters)
hin.GetLinkGroup('Crecos').info

## Testing Pure Popularity:
parameters['seen_relation']='rates'
parameters['method']='IPP'
hin.CreateLinkGroupFromRS('likes','PPrecos',parameters)
hin.GetLinkGroup('PPrecos').info

# Testing content-based recommender (based on Pathsim)
parameters['method']='CB'
parameters['paths'] = [['likes','is_directed','inverse_is_directed'],
         ['likes','is_of_type','inverse_is_of_type'],
         ['likes','has_actor','inverse_has_actor']]
parameters['paths_weights'] = [1/3,1/3,1/3]
hin.CreateLinkGroupFromRS('likes','CBrecos',parameters)
hin.GetLinkGroup('CBrecos').info

# Testing random recommendations
parameters['method']='random'
hin.CreateLinkGroupFromRS('likes','random_recos',parameters)

# Testing classic recommendations metrics

surp  = hin.SurprisalDivMes('Crecos','likes')
uinov = hin.NoveltyDivMes('Crecos','inverse_rates')
itnov = hin.NoveltyDivMes('Crecos','is_of_type')
ils = hin.IntraListSimilarityDivMes('Crecos','is_of_type')
per = hin.PersonalisationDivMes('Crecos')

# retrieve the table of a link group
recos_table=hin.table[hin.table.relation=='CBrecos']
rates_table=hin.table[hin.table.relation=='rates']


        
