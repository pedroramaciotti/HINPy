

import hinpy


import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = "raise"


# Format of the dataset
#
# COLUMNS:
# link grou name
# start object group
# start object
# end object group
# end object
# value associated to the link (score, rating)

#
# Examples
#
#
# is_friend,user,u1,user,u2,
# is friend,user,u2,user,u3
# rates,user,u1,item,i1,4
# rates,user,u1,item,i2,4
# rates,user,u2,item,i2,3
# rates,user,u3,item,i3,5
# has_type,item,i1,type,t1
# has_type,item,i1,type,t2
# has_type,item,i2,type,t2
# has_type,item,i3,type,t3
#

# Loading the dataset
hin = hinpy.classes.HIN(name='m100k',filename='datasets/movielens100k_hin.csv',inverse_relations=True)


# Creating a Link Group "likes" from rates
def likes_func(x):
    if x<3:
        return False;
    else:
        return True;
hin.CreateLinkGroupFromLinkGroup(relation_name='rates',new_relation_name='likes',condition_method=likes_func)


# Computing recommendations

#    1. UBCF
params = {'method':'UBCF', 'min_scale':1, 'max_scale':5, 'model_size':10, 'topK_predictions': 4, 'RMSE':True}
hin.CreateLinkGroupFromRS(relation_name='rates',new_relation_name='UBCF-recos',parameters=params)
print('UBCF recommendations computed with RMSE = %.2f'%hin.GetLinkGroup('UBCF-recos').info['RMSE'])
#    2. NMF
params = {'method':'NMF', 'min_scale':1, 'max_scale':5, 'model_size':10, 'topK_predictions': 4, 'RMSE':True}
hin.CreateLinkGroupFromRS(relation_name='rates',new_relation_name='NMF-recos',parameters=params)
print('NMF recommendations computed with RMSE = %.2f'%hin.GetLinkGroup('NMF-recos').info['RMSE'])
#    3. Pure Popularity
params = {'method':'IPP', 'topK_predictions': 4, 'seen_relation':'rates'}
hin.CreateLinkGroupFromRS(relation_name='likes',new_relation_name='PP-recos',parameters=params)
print('PP recommendations computed.')
#    4. Content based
params = {'method':'CB', 'topK_predictions': 4, 'seen_relation':'rates', 'paths':[['likes','is_of_type','inverse_is_of_type']], 'paths_weights':[1]}
hin.CreateLinkGroupFromRS(relation_name='likes',new_relation_name='CB-recos',parameters=params)
print('CB recommendations computed.')
#    5. Random recommendations
params = {'method':'random', 'topK_predictions': 4, 'seen_relation':'rates'}
hin.CreateLinkGroupFromRS(relation_name='likes',new_relation_name='random-recos',parameters=params)
print('random recommendations computed.')

print('The new HIN schema is:')
print(hin.GetLinkGroupsNames())


# Computing classic diversity measures
print('')
for link_group in ['UBCF-recos','NMF-recos','PP-recos','CB-recos','random-recos']:
    surprisal       = hin.SurprisalDivMes(            relation_name=link_group,  popularity_relation_name='likes')
    ui_novelty      = hin.NoveltyDivMes(              relation_name=link_group,  similarity_relation='inverse_rates')
    it_novelty      = hin.NoveltyDivMes(              relation_name=link_group,  similarity_relation='is_of_type')
    ils             = hin.IntraListSimilarityDivMes(  relation_name=link_group,  similarity_relation='is_of_type')
    personalisation = hin.PersonalisationDivMes(      relation_name=link_group)
    print('%s :'%link_group)
    print('Suprisal: %.2f \t Novelty(UI): %.2f \t Novelty(IT): %.2f \t ILS: %.2f \t Perso.: %.2f'%(surprisal,ui_novelty,it_novelty,
                                                                                                   ils,personalisation))



# Computing HIN diversities
print('')

# Available diversity (collective IT)
available = hin.GetSetCollectiveTrueDiversity(relation_list=['is_of_type'],alpha=1)
# Consumed diversity
col_consumed = hin.GetSetCollectiveTrueDiversity(relation_list=['rates','is_of_type'],alpha=1)
mi_consumed = hin.GetSetMeanIndTrueDiversity(relation_list=['rates','is_of_type'],alpha=1,method='geo')
# Preferred diversity
col_preferred = hin.GetSetCollectiveTrueDiversity(relation_list=['likes','is_of_type'],alpha=1)
mi_preferred = hin.GetSetMeanIndTrueDiversity(relation_list=['likes','is_of_type'],alpha=1,method='geo')
# Recommended diversity
ubcf_col_preferred = hin.GetSetCollectiveTrueDiversity(relation_list=['UBCF-recos','is_of_type'],alpha=1)
ubcf_mi_preferred = hin.GetSetMeanIndTrueDiversity(relation_list=['UBCF-recos','is_of_type'],alpha=1,method='geo')
nmf_col_preferred = hin.GetSetCollectiveTrueDiversity(relation_list=['NMF-recos','is_of_type'],alpha=1)
nmf_mi_preferred = hin.GetSetMeanIndTrueDiversity(relation_list=['NMF-recos','is_of_type'],alpha=1,method='geo')
pp_col_preferred = hin.GetSetCollectiveTrueDiversity(relation_list=['PP-recos','is_of_type'],alpha=1)
pp_mi_preferred = hin.GetSetMeanIndTrueDiversity(relation_list=['PP-recos','is_of_type'],alpha=1,method='geo')
cb_col_preferred = hin.GetSetCollectiveTrueDiversity(relation_list=['CB-recos','is_of_type'],alpha=1)
cb_mi_preferred = hin.GetSetMeanIndTrueDiversity(relation_list=['CB-recos','is_of_type'],alpha=1,method='geo')
random_col_preferred = hin.GetSetCollectiveTrueDiversity(relation_list=['random-recos','is_of_type'],alpha=1)
random_mi_preferred = hin.GetSetMeanIndTrueDiversity(relation_list=['random-recos','is_of_type'],alpha=1,method='geo')

print('                    Mean Ind.\t Collective')
print('--------------------------------------------')
print('Available diversity :         \t %.2f'%available)
print('Consumed diversity  :    %.2f \t %.2f'%(mi_consumed,col_consumed))
print('Preferred diversity :    %.2f \t %.2f'%(mi_preferred,col_preferred))
print('Recommended (UBCF)  :    %.2f \t %.2f'%(ubcf_mi_preferred,ubcf_col_preferred))
print('Recommended (NMF)   :    %.2f \t %.2f'%(nmf_mi_preferred,nmf_col_preferred))
print('Recommended (PP)    :    %.2f \t %.2f'%(pp_mi_preferred,pp_col_preferred))
print('Recommended (CB)    :    %.2f \t %.2f'%(cb_mi_preferred,cb_col_preferred))
print('Recommended (random):    %.2f \t %.2f'%(random_mi_preferred,random_col_preferred))
     
