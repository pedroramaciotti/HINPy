import hinpy


import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = "raise"
from random import choice
from hinpy.rs.implicit_utility import *

likes_func = lambda x: True if x>2.5 else False

hin = hinpy.classes.HIN(name='m100k',filename='datasets/movielens100k_hin.csv',inverse_relations=True)
hin.CreateLinkGroupFromLinkGroup(relation_name='rates',new_relation_name='likes',condition_method=likes_func)

#
# Separate Link Group in Train and Test parts
# Chose K for topK recommendations: L_u(K) = RS(N,u)
# Recall_u    = #{links in L_u(K) that are also in T_u}/#{T_u}  ---K \infty --> 1
# Precision_u = #{links in L_u(K) that are also in T_u}/#{L_u(K)} ---K \infty --> 0
# What's the best strategy for HINPy?
# - Separate actual RS and testing
# - This means creating another method, elsewhere, that will use the CB RS
# - Where? Normal functioning is:
#    - one calls CreateLinkGroupFromRS, which calls HINRS and gives predicted table and metrics
#    - report is what's used for surprise-based metrics
#    - so it should be inside HINRS: yes, and then we only call ContentBased


params = {'method':'CB', 'topK_predictions': 4, 'seen_relation':'rates', 
#          'paths':[['likes','is_of_type','inverse_is_of_type'],
#                   ['inverse_has_occupation','has_occupation','likes']], 
#                   'paths_weights':[0.75,0.25],
          'paths':[['likes','is_of_type','inverse_is_of_type']], 
          'paths_weights':[1],
          'implicit_metrics':True,'implicit_metrics_N':[5,10,15,20,25,30,35,40,45,50],
          'implicit_metrics_fraction':0.25}
hin.CreateLinkGroupFromRS(relation_name='likes',new_relation_name='CB-recos',parameters=params)

#_,test_subtable,reco_subtable=ImplicitUtilityMetrics(hin,'likes',parameters=params)
#
#q = pd.DataFrame(columns=['object','precision','recall','f1'])
#q['object'] = test_subtable.start_object.unique()
#for idx,row in q.iterrows():
#    Cu = set(test_subtable[test_subtable.start_object==row.object].end_object)
#    Lu = set(reco_subtable[reco_subtable.start_object==row.object].end_object)
#    q.loc[idx,'recall'] = len(Cu&Lu)/len(Cu)
#    q.loc[idx,'precision'] = len(Cu&Lu)/len(Lu)
#
#
#raise
#
## Compute Quality Values
#q = pd.DataFrame(columns=['object','tp','fn','fp','tn','precision','recall','f1'])
#q['object'] = true_table.start_object.unique()
#
#for idx,row in q.iterrows():
#    Cu = set(true_table[true_table.start_object==row.object].end_object)
#    Lu = set(rs_table[rs_table.start_object==row.object].end_object)
#    q.loc[idx,'tp'] = len(Cu&Lu)
#    q.loc[idx,'fn'] = len(Cu-Lu)
#    q.loc[idx,'fp'] = len(Lu-Cu)
##    q.loc[idx,'tn'] = len() # Not used
#q['precision'] = q.apply(lambda row: row.tp/(row.tp+row.fp),axis=1)
#q['recall'] = q.apply(lambda row: row.tp/(row.tp+row.fn),axis=1)
#
#precision = q['precision'].mean()
#recall = q['recall'].mean()
#
#f1 = 2*precision*recall/(precision+recall)