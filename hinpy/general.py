import pandas as pd



def FirstAbsentNumberInList(input_list):
    for id_candidate in range(max(input_list)+2):
        if id_candidate not in input_list:
            return id_candidate;


def VerboseMessage(verbose,message):
    if verbose:
        print(message)
    return;

def ETSec2ETTime(s):
    s=int(s)
    # days, remainder = divmod(s,3600*24)
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds));
