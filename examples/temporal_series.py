import sys
sys.path.append('/Users/pedroramaciotti/Programs/HINPy/')
import hinpy


# Load 
hin = hinpy.classes.HIN(name='m100k',filename='/Users/pedroramaciotti/Programs/HINPy/datasets/movielens100k_hin.csv',inverse_relations=False)

# Time series of rates
table=hin.table[hin.table.relation=='rates']

year =  [1997,1997,1997,1997,1998,1998,1998,1998]
month = [9,10,11,12,1,2,3,4]