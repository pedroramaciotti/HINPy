

import hinpy
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = "raise"

#hin = hinpy.classes.HIN(name='example',filename='datasets/example1.csv',verbose=False,inverse_relations=True)
#hin = hinpy.classes.HIN(name='douban movie',filename='datasets/douban_movie_hin.csv',verbose=False,inverse_relations=True)
#hin = hinpy.classes.HIN(name='m100k',filename='datasets/movielens100k_hin.csv',verbose=False,inverse_relations=True)
hin = hinpy.classes.HIN(name='yelp',filename='datasets/yelp_hin.csv',verbose=False,inverse_relations=True)
#hin = hinpy.classes.HIN(name='amazon',filename='datasets/amazon_digital_music_hin.csv',verbose=False,inverse_relations=True)
#hin = hinpy.classes.HIN(name='ml1M',filename='../../DataBases/MovieLens/ml-1m/movielens1M_hin.csv',verbose=False,inverse_relations=True)

raise

p=hin.GetPathProportionalAbundance(['rates','is_of_type'])

def likes(x):
    if x<3:
        return False;
    else:
        return True;
    
    
hin.CreateLinkGroupFromLinkGroup('rates','likes',likes,verbose=True)

## Testing UBCF:
parameters = {}
parameters['method']='IBCF'
parameters['min_scale']=1
parameters['max_scale']=5
parameters['model_size']=3
parameters['prefilter_score']=False
parameters['prefilter_threshold']=3.5
parameters['topK_predictions']=4
parameters['RMSE']=True
hin.CreateLinkGroupFromRS('rates','recos',parameters,verbose=False)
hin.GetLinkGroup('recos').info

## Testing PP:
parameters['seen_relation']='rates'
parameters['method']='IPP'
hin.CreateLinkGroupFromRS('likes','PPrecos',parameters,verbose=True)
hin.GetLinkGroup('PPrecos').info

# Testing CB
parameters['method']='CB'
parameters['paths'] = [['likes','is_directed','inverse_is_directed'],
         ['likes','is_of_type','inverse_is_of_type'],
         ['likes','has_actor','inverse_has_actor']]
parameters['paths'] = [['likes','is_of_type','inverse_is_of_type']]
parameters['paths_weights'] = [1/3,1/3,1/3]
parameters['paths_weights'] = [1]

hin.CreateLinkGroupFromRS('likes','CBrecos',parameters,verbose=True)
hin.GetLinkGroup('CBrecos').info

# Testing random RS
parameters['method']='random'
hin.CreateLinkGroupFromRS('likes','random_recos',parameters,verbose=True)

# Testing Diversity Measures

si  = hin.SurprisalDivMes('recos','likes')

uinov = hin.NoveltyDivMes('recos','inverse_rates')
itnov = hin.NoveltyDivMes('recos','is_of_type')

ils = hin.IntraListSimilarityDivMes('recos','is_of_type')

per = hin.PersonalisationDivMes('recos')

# testing 



# Table
table = hin.table.copy(deep=True)
recos_table=hin.table[hin.table.relation=='recos']
rates_table=hin.table[hin.table.relation=='rates']


        
