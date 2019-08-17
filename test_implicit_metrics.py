import hinpy


import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = "raise"
from random import choice


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
# - Where? 


# create random df
users = ['a','b','c','d']
items = ['i%s'%n for n in range(20)]
i_per_u = 4
u=[]
i=[]
for user in users:
    for n in range(i_per_u):
        u.append(user)
        i.append(np.random.choice(items))
df = pd.DataFrame(data={'user':u,'item':i})

df_grouped = df.groupby('user')
df_test  = df_grouped.apply(lambda x: x.sample(frac=0.25)).reset_index(drop=True)
df_train = df[~df.apply(tuple,1).isin(df_test.apply(tuple,1))].reset_index(drop=True)


# Test splitting LinkGroup
fraction=0.25
subtable = hin.table[hin.table.relation=='likes'].drop_duplicates()
subtable = subtable[subtable.columns[:-1]]
dup_subtable = subtable[subtable.duplicated()]
grouped = subtable.groupby('start_object')
test_subtable = grouped.apply(lambda x: x.sample(frac=fraction)).reset_index(drop=True)
train_subtable = subtable[~subtable.apply(tuple,1).isin(test_subtable.apply(tuple,1))].reset_index(drop=True)

test_tuples = list(test_subtable.apply(tuple,1))
train_tuples = list(train_subtable.apply(tuple,1))


print('subtable : %d'%subtable.shape[0])
print('test_subtable : %d'%test_subtable.shape[0])
print('train_subtable : %d'%train_subtable.shape[0])
print('train+test : %d'%(train_subtable.shape[0]+test_subtable.shape[0]))
print('duplicates : %d'%subtable[subtable.duplicated()].shape[0])
print('missing: %d'%(subtable.shape[0]-(train_subtable.shape[0]+test_subtable.shape[0])))

# There are 11 rows in subtable that are not in neither, train nor test

problematic=[]
for idx,row in subtable.iterrows():
    raise
    if tuple(row) in test_tuples:
        continue
    if tuple(row) in train_tuples:
        continue
    problematic.append(row)
        


raise


hin.CreateSubsampledLinkGroup('rates','ss_rates',fraction=0.5,per_start_object=True)


hin.CreateLinkGroupFromLinkGroup(relation_name='ss_rates',new_relation_name='ss_likes',condition_method=likes_func)
params={'topK_predictions':10,'method':'CB', 'paths':[['ss_likes','is_of_type','inverse_is_of_type']],'paths_weights':[1],'seen_relation':'ss_rates'}
hin.CreateLinkGroupFromRS(relation_name='ss_likes',new_relation_name='ss_CB',parameters=params)


rs_table   = hin.table[hin.table.relation=='ss_CB'].copy(deep=True)
true_table = hin.table[hin.table.relation=='likes'].copy(deep=True)

# Compute Quality Values
q = pd.DataFrame(columns=['object','tp','fn','fp','tn','precision','recall','f1'])
q['object'] = true_table.start_object.unique()

for idx,row in q.iterrows():
    Cu = set(true_table[true_table.start_object==row.object].end_object)
    Lu = set(rs_table[rs_table.start_object==row.object].end_object)
    q.loc[idx,'tp'] = len(Cu&Lu)
    q.loc[idx,'fn'] = len(Cu-Lu)
    q.loc[idx,'fp'] = len(Lu-Cu)
#    q.loc[idx,'tn'] = len() # Not used
q['precision'] = q.apply(lambda row: row.tp/(row.tp+row.fp),axis=1)
q['recall'] = q.apply(lambda row: row.tp/(row.tp+row.fn),axis=1)

precision = q['precision'].mean()
recall = q['recall'].mean()

f1 = 2*precision*recall/(precision+recall)