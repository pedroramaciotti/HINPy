import pandas as pd


class ObjectGroup:
    """
    ObjectGroup

    Attributes:
    -----------
    name : str
        Name of the group of objects.
    id : int
        Global id of the group of objects.
    size : int
        Number of objects in the group.
    objects_ids_queue : list[int]
        List with the current order of the objects' ids.
    objects_names : dic{int:str}
        Dictionary with the names of the objects indexed by their ids.
    """
    def __init__(self, object_list, name, id):
        self.name = name
        self.id   = id
        self.size = len(object_list)
        self.objects_ids_queue = list(range(self.size))
        self.objects_names  = {}
        self.objects_ids  = {}
        for object_id in self.objects_ids_queue:
            self.objects_names[object_id] = object_list[object_id]
            self.objects_ids[object_list[object_id]] = object_id
        return;

    #
    # Retrievers
    #

    def GetObjectQueuePos(self,name):
        return self.objects_ids_queue.index(self.objects_ids[name]);

    def GetNames(self):
        return [k for k,v in self.objects_ids.items()];
