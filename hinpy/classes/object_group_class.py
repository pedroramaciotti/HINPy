import pandas as pd

from time import time as TCounter

from hinpy.general import *

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
    def __init__(self, object_list, name, id,verbose=False):
        t=TCounter()
        VerboseMessage(verbose,'Building Object Group %s...'%name)
        self.name = name
        self.info = {}
        self.id   = id
        self.object_list = object_list
        self.size = len(object_list)
        self.objects_ids_queue = list(range(self.size))
        self.objects_names  = {} # dictionary taking ids and giving object name
        self.objects_ids  = {} # dictionary taking object name and giving idi
        for object_id in self.objects_ids_queue:
            self.objects_names[object_id] = object_list[object_id]
            self.objects_ids[object_list[object_id]] = object_id
        VerboseMessage(verbose,'Object Group %s built in %s.'%(name,ETSec2ETTime(TCounter()-t)))
        return;

    #
    # Retrievers
    #

    def GetObjectQueuePos(self,name):
        return self.objects_ids_queue.index(self.objects_ids[name]);

    def GetNames(self):
        return [k for k,v in self.objects_ids.items()];

    def OjectPositionDicFromName(self):
        object_position = {}
        for obj,idx in self.objects_ids.items():
            object_position[obj]=self.GetObjectQueuePos(obj)
        return object_position;

    def OjectNameDicFromPosition(self):
        object_name = {}
        for obj,idx in self.objects_ids.items():
            object_name[self.GetObjectQueuePos(obj)]=obj
        return object_name;
