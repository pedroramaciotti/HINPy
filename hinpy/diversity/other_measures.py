import pandas as pd
import numpy as np

from time import time as TCounter

from hinpy.general import *



def Surprisal(popularity_table,recommended_table,verbose=False):

    """
    From:
    ZHOU, Tao, KUSCSIK, Zoltán, LIU, Jian-Guo, et al.
    Solving the apparent diversity-accuracy dilemma of recommender systems.
    Proceedings of the National Academy of Sciences,
    2010, vol. 107, no 10, p. 4511-4515.
    """

    if verbose:
        t=TCounter()
        VerboseMessage(verbose,'Computing Surprisal of %s relative to %s...'%(recommended_table.relation.iloc[0],popularity_table.relation.iloc[0]))
    # Computing self-information for each end objects based on previous choices
    popularity_table.loc[:,'degree']=1
    end_object_si=popularity_table[['end_object','degree']].groupby('end_object').count()
    number_of_start_objects=popularity_table.start_object.unique().size
    end_object_si=end_object_si.apply(lambda x: np.log2(number_of_start_objects/x))
    recommended_table=recommended_table[recommended_table.end_object.isin(end_object_si.index)].copy(deep=True)
    # Checking that all recommended end objects have a self-information value
    if not np.isin(recommended_table.end_object.unique(),popularity_table.end_object.unique()).all():
        raise ValueError('Some recommended end objects do not have self-information value.')
        # print('WARNING: Some recommended end objects do not have self-information value.')
    # Computing each list's self-information
    recommended_table['end_object_si']=recommended_table.end_object.map(end_object_si.iloc[:,0]).copy(deep=True).values
    # Surpisal is then the mean self-information for all users
    surprisal = recommended_table['end_object_si'].mean()

    if verbose:
        VerboseMessage(verbose,'Surprisal computed in %s.'%(ETSec2ETTime(TCounter()-t)))
    return surprisal;


def Novelty(recommended_table,similarity_matrix,object_position,verbose=False):
    """
    From:
    Equation (2) of
    HURLEY, Neil et ZHANG, Mi.
    Novelty and diversity in top-n recommendation--analysis and evaluation.
    ACM Transactions on Internet Technology (TOIT), 2011, vol. 10, no 4, p. 14.

    - The novelty of each item in the list is computed with respect to all other
    items in the list. This results in a novelty value for each recommended list.
    - The global novelty is the mean of the novelty of the lists.
    - The distance d is computed as a dissimilarity, i.e.:
            d = 1 - similarity
      where the similarity is the cosine similarity given to the funcion as a
      similarity matrix.
    """
    if verbose:
        t=TCounter()
        VerboseMessage(verbose,'Computing Novelty of %s...'%(recommended_table.relation.iloc[0]))
    # Create DataFrame with information on each start object needed for the computation
    start_object_data = pd.DataFrame()
    # Get names of objects
    start_object_data['object']=recommended_table.start_object.unique()
    # Get the recommendation list made to each object
    reco_lists = recommended_table[['start_object','end_object']].groupby('start_object')['end_object'].apply(list)
    start_object_data['reco_list']=start_object_data['object'].map(reco_lists)
    # Get the list size
    start_object_data['list_size']=start_object_data['reco_list'].apply(len)
    # Checking list_size
    start_object_data=start_object_data[start_object_data.list_size>1].copy(deep=True)
    # Compute de dissimilarity of the list using the similarity matrix
    start_object_data['dissimilarity']=start_object_data['reco_list'].apply(lambda x: dissimilarity(similarity_matrix,x,object_position))
    # Compute the novelty
    start_object_data['novelty']=start_object_data.apply(lambda x: x.dissimilarity/(x.list_size*(x.list_size-1)),axis=1)
    # Return the mean novelty of all recommendation lists
    novelty = start_object_data['novelty'].mean()
    if verbose:
        VerboseMessage(verbose,'Novelty computed in %s.'%(ETSec2ETTime(TCounter()-t)))
    return novelty;

def IntraListSimilarity(recommended_table,similarity_matrix,object_position,verbose=False):
    """
    ZIEGLER, Cai-Nicolas, MCNEE, Sean M., KONSTAN, Joseph A., et al.
    Improving recommendation lists through topic diversification.
    Proceedings of the 14th international conference on World Wide Web.
    ACM, 2005. p. 22-32.
    """
    if verbose:
        t=TCounter()
        VerboseMessage(verbose,'Computing Intra-List Similarity of %s...'%(recommended_table.relation.iloc[0]))
    # Create DataFrame with information on each start object needed for the computation
    start_object_data = pd.DataFrame()
    # Get names of objects
    start_object_data['object']=recommended_table.start_object.unique()
    # Get the recommendation list made to each object
    reco_lists = recommended_table[['start_object','end_object']].groupby('start_object')['end_object'].apply(list)
    start_object_data['reco_list']=start_object_data['object'].map(reco_lists)
    # Compute de Intra List Similarity of the list using the similarity matrix
    start_object_data['ILS']=start_object_data['reco_list'].apply(lambda x: similarity(similarity_matrix,x,object_position))
    # Return the mean Intra List Similarity of all recommendation lists
    ILS = start_object_data['ILS'].mean()
    if verbose:
        VerboseMessage(verbose,'Intra-List Similarity computed in %s.'%(ETSec2ETTime(TCounter()-t)))
    return ILS;

def Personalisation(recommended_table,verbose=False):
    """
    From:
    ZHOU, Tao, KUSCSIK, Zoltán, LIU, Jian-Guo, et al.
    Solving the apparent diversity-accuracy dilemma of recommender systems.
    Proceedings of the National Academy of Sciences,
    2010, vol. 107, no 10, p. 4511-4515.
    """
    if verbose:
        t=TCounter()
        VerboseMessage(verbose,'Computing Personalisation of %s...'%(recommended_table.relation.iloc[0]))
    # Creating alias for end objects
    end_objects = recommended_table['end_object'].unique()
    recommended_table['alias']=recommended_table['end_object'].map(pd.Series(index=end_objects,data=range(end_objects.size)))
    # Create DataFrame with information on each start object needed for the computation
    start_object_data = pd.DataFrame()
    # Get names of objects
    start_object_data['object']=recommended_table.start_object.unique()
    # Get the recommendation list made to each object
    reco_lists = recommended_table[['start_object','alias']].groupby('start_object')['alias'].apply(list)
    start_object_data['reco_list']=start_object_data['object'].map(reco_lists)
    L = list(start_object_data['reco_list'])
    counter=0
    personalisation=0
    for i in range(len(L)-1):
        for j in range(i+1,len(L)-1):
            personalisation+= 1- jaccard(L[i],L[j])
            counter+=1
    personalisation = personalisation/counter
    if verbose:
        VerboseMessage(verbose,'Personalisation computed in %s.'%(ETSec2ETTime(TCounter()-t)))
    return personalisation;


############################################
# Functions used by the diversity measures #
############################################

def jaccard(Li,Lj):
    return len(set(Li)&set(Lj))/len(set(Li)|set(Lj));

def dissimilarity(matrix,L,ids):
    d=0
    for i in L:
        for j in L:
            if i!=j:
                d+= 1-matrix[ids[i],ids[j]]
    return d;

def similarity(matrix,L,ids):
    s=0
    for i in L:
        for j in L:
            if i!=j:
                s+= 0.5*matrix[ids[i],ids[j]]
    return s;
