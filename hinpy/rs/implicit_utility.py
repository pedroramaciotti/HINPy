import pandas as pd
import numpy as np

from hinpy.classes.hin_class import *

from hinpy.rs.pure_popularity import *
from hinpy.rs.content_based import *
from hinpy.rs.surprise_based import *
from hinpy.rs.random_rs import *


def ImplicitUtilityMetrics(hin,relation_name,parameters,verbose=False):
	"""
	Compute precision, recall, an F1 for implicit RS (IPP,CB,random).

	"""

	# Retrieve the table of relation_name and separate into test and train parts
	if 'implicit_metrics_fraction' in parameters:
		fraction = parameters['implicit_metrics_fraction']
	else:
		fraction = 0.25

	subtable = hin.table[hin.table.relation==relation_name]
	subtable = subtable[subtable.columns[:-1]]
	dup_subtable = subtable[subtable.duplicated()]
	grouped = subtable.groupby('start_object')

	test_subtable = grouped.apply(lambda x: x.sample(frac=fraction)).reset_index(drop=True)
	train_subtable = subtable[~subtable.apply(tuple,1).isin(test_subtable.apply(tuple,1))].reset_index(drop=True)

	train_subtable.loc[:,'relation'] = 'train_link_group'

	# Create train Link Group from table
	hin.CreateLinkGroupFromTable(train_subtable,'train_link_group')

	# Create new 'seen' table subtracting elements from test
	seen_table = hin.table[hin.table.relation==parameters['seen_relation']].copy(deep=True)
	seen_table.loc[:,'relation'] = test_subtable.relation.iloc[0]
	seen_table = seen_table[~seen_table.apply(tuple,1).isin(test_subtable.apply(tuple,1))].reset_index(drop=True)
	hin.CreateLinkGroupFromTable(seen_table,'train_seen_group')

	# For n in 'implicit_metrics_N':[1,5,10], compute recos
	# and compute recall and precision per start object
	report_dic = {'topK':parameters['implicit_metrics_N']}
	precision = np.zeros(len(parameters['implicit_metrics_N']))
	recall = np.zeros(len(parameters['implicit_metrics_N']))
	f1 = np.zeros(len(parameters['implicit_metrics_N']))
	reco_train_params = {'method':'CB', 'topK_predictions': 4, 'seen_relation':'rates',
          'paths':parameters['paths'],
          'paths_weights':parameters['paths_weights'],
          'implicit_metrics':False}
	for i,k in enumerate(parameters['implicit_metrics_N']):
		reco_train_params['topK_predictions']=k
		hin.CreateLinkGroupFromRS(relation_name='train_link_group',
								  new_relation_name='implicit_metrics_recs_%d'%k,
								  parameters=reco_train_params)
		# Here, compute precision, recall and f1
		reco_subtable = hin.table[hin.table.relation=='implicit_metrics_recs_%d'%k].copy(deep=True)
		q = pd.DataFrame(columns=['object','precision','recall','f1'])
		q['object'] = test_subtable.start_object.unique()
		for idx,row in q.iterrows():
		    Cu = set(test_subtable[test_subtable.start_object==row.object].end_object)
		    Lu = set(reco_subtable[reco_subtable.start_object==row.object].end_object)
		    q.loc[idx,'recall'] = len(Cu&Lu)/len(Cu)
		    q.loc[idx,'precision'] = len(Cu&Lu)/len(Lu)
		precision[i] = q['precision'].mean()
		recall[i] = q['recall'].mean()
		f1[i] = 2*precision[i]*recall[i]/(precision[i]+recall[i])

		# Delete the recommendation
		hin.DeleteLinkGroup('implicit_metrics_recs_%d'%k)
	# Delete train Link Group
	hin.DeleteLinkGroup('train_link_group')
	hin.DeleteLinkGroup('train_seen_group')

	report_dic['precision'] = precision
	report_dic['recall'] = recall
	report_dic['f1'] = f1

	return report_dic;
