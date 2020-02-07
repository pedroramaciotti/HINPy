![logo](https://raw.githubusercontent.com/pedroramaciotti/HINPy/master/docs/logo.png)

## HINPy: Heterogeneous Information Networks for Python

A framework for the extracting metrical, hilbertian, and probability space structures from topological models.


### Installation
After you download the project, execute:

- `pip install .` 

in the parent folder. Equivalently, you can just execute:

- `pip install git+https://github.com/pedroramaciott/HINPy`


### Quickstart

#### A simple example

![logo](https://raw.githubusercontent.com/pedroramaciotti/HINPy/master/docs/simple_example.png)

File available in *datasets* as simple_example.csv

    likes,user,u1,item,i1,,
    likes,user,u1,item,i2,,
    likes,user,u2,item,i3,,
    likes,user,u3,item,i4,,
    likes,user,u3,item,i5,,
    recommended,user,u1,item,i3,,
    recommended,user,u2,item,i1,,
    recommended,user,u2,item,i4,,
    recommended,user,u3,item,i2,,
    recommended,user,u3,item,i3,,
    classification,item,i1,type,t1,,
    classification,item,i2,type,t2,,
    classification,item,i4,type,t2,,
    classification,item,i4,type,t3,,
    classification,item,i5,type,t3,,

#### A second example

![logo](https://raw.githubusercontent.com/pedroramaciotti/HINPy/master/docs/example.png)

File available in *datasets* as example.csv:

    E0,V0,v01,V2,v11,,
    E0,V0,v02,V2,v12,,
    E0,V0,v02,V2,v13,,
    E1,V1,v11,V2,v23,,
    E1,V1,v11,V2,v24,,
    E1,V1,v12,V2,v24,,
    E2,V2,v21,V3,v31,,
    E2,V2,v21,V3,v32,,
    E2,V2,v21,V3,v32,,
    E2,V2,v22,V3,v33,,
    E2,V2,v22,V3,v34,,
    E2,V2,v23,V3,v33,,
    E2,V2,v24,V3,v33,,
    E2,V2,v24,V3,v34,,
    E3,V3,v31,V4,v41,,
    E3,V3,v32,V4,v42,,
    E4,V3,v32,V5,v51,,
    E4,V3,v34,V5,v52,,
    E4,V3,v34,V5,v52,,
    E5,V1,v11,V5,v51,,
    E5,V1,v12,V5,v52,,
    E5,V1,v12,V5,v53,,
