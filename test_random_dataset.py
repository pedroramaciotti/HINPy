

import hinrecodiv as nrd



object_data=[('user',20),('item',20),('genre',5)]
link_data=[('rates','user','item',0.05),('belongs','item','genre',0.1)]
parameters={}

a,b=nrd.datasets.random_hin_generator(object_data,link_data)