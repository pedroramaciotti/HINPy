def FirstAbsentNumberInList(input_list):
    for id_candidate in range(max(input_list)+2):
        if id_candidate not in input_list:
            return id_candidate;
