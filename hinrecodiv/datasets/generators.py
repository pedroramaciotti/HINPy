import numpy as np
import pandas as pd


def random_hin_generator(object_data,link_data):
    # Format:
    # object_data: list of 2-tuples with name (str) of the object type and
    # number (int) of objects of that type
    # object_link: list of 4-tuples with name (str) of link type,
    # the name of the starting object type (str), the name of the ending object
    # type (str), and the density (float) of the relation.

    # Initial Checks
    #
    #
    #
    #
    #
    #
    #


    # Retrieving object data
    object_type_name = []
    object_type_size = []
    for name,size in object_data:
        object_type_name.append(name)
        object_type_size.append(size)

    # Retrieving link data
    link_type_name = []
    link_type_start = []
    link_type_end = []
    link_type_density = []
    for name,start,end,density in link_data:
        link_type_name.append(name)
        link_type_start.append(start)
        link_type_end.append(end)
        link_type_density.append(density)
        
    df = pd.DataFrame(columns=['link type','start type','start','end type','end','score','timestamp'])        

        
    # For each link type, compute the number of links for density and put them 
    # into the dataframe
    for i,link_type in enumerate(link_type_name):
        start_index=object_type_name.index(link_type_start[i])
        end_index=object_type_name.index(link_type_end[i])
        number_of_links = int(object_type_size[start_index]*object_type_size[end_index]*link_type_density[i])
        print(link_type)
        print(number_of_links)

    return object_type_name,object_type_size;
