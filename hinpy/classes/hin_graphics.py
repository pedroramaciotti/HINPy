import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt



def plot_hin(table,filename=None,
	node_size=700,layout='spring',arrowsize=10,
	edge_labels=True,node_labels=True):

	g = nx.MultiDiGraph()
	for _,row in table.iterrows():
	    g.add_edge(row.start_group,row.end_group,label=row.relation)

	if layout=='spring':
		pos = nx.spring_layout(g)
	elif layout=='spectral':
		pos = nx.spectral_layout(g)
	elif layout=='random':
		pos = nx.random_layout(g)
	elif layout=='shell':
		pos = nx.shell_layout(g)
	else:
		raise ValueError('Layout %s not recognized.'%layout)
	
	edge_labels = { (u,v): d['label'] for u,v,d in g.edges(data=True) }
	 
	nx.draw_networkx_nodes(g,pos,node_size=node_size,arrowsize=arrowsize)
	nx.draw_networkx_edges(g,pos)
	if node_labels:
		nx.draw_networkx_labels(g,pos)
	if edge_labels:
		nx.draw_networkx_edge_labels(g,pos,edge_labels=edge_labels)
	plt.axis('off')
	if filename is not None:
		plt.savefig(filename)
	else:
		plt.show()

	return;