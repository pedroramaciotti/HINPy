![logo](https://raw.githubusercontent.com/pedroramaciotti/HINPy/master/docs/logo.png)

## HINPy: Heterogeneous Information Networks for Python

**In short:** HINPy is a python workbench for Heterogeneous Information Networks (graphs with colored nodes and edges) suited for the analysis of Recommender Systems (accuracy, diversity, similarity), and network representation in other domains (e.g, ecology, scientometrics, social network analysis).

**In long[er]:**HINPy is a framework that provides a flexible ontology to topological data (entities of different type connected/related by different relations), and allows for the extraction of metrical (similarities, distances), hilbertian (embedding in spaces with relative order), and bayesian (empirical distributions and apportionments) structures.

It also provides [experimental] functionalities to perform recommendations using classic Recommender Systems, and evaluate recommendations with classic diversity metrics.

Also experimental is the extraction of timeseries of apportionments and aggregations such as diversity measures.

### Installation
After you download the project, execute:

- `pip install .` 

in the parent folder. Equivalently, you can just execute:

- `pip install git+https://github.com/pedroramaciott/HINPy`


### Quickstart

#### Syntax

You can name related entities in lines in a CSV file as:

`relation_name,group_of_entity1,name_of_entity1,group_of_entity2,name_of_entity2,some_value,timestamp`.

Values (some_value) and timestamps are optional (in case you want to do some filtering or timeseries). In a Recommender Systems setting, for example, you can name your entities and relations as:

    has_chosen,users,user1,items,item1,5.0,1990
    has_chosen,users,user1,items,item2,3.0,1991
    ...
    was_recommended,user1,items,item4,,
    ...
    is_of_type,items,i1,type,t1,,
    ...

if you want to declared users that chose/ranked some items (e.g., films) at some time, and items that belong to categories (e.g., genres).

You can then load your CSV (without header nor index):

    import hinpy 

    hin = hinpy.classes.HIN(filename=path_to_your_csv_file)


*The remainder of this README is under construction...*

#### A simple example

![logo](https://raw.githubusercontent.com/pedroramaciotti/HINPy/master/docs/simple_example.png)

File available in *datasets* as `simple_example.csv`:

    E0,V0,u1,V1,i1,,
    E0,V0,u1,V1,i2,,
    E0,V0,u2,V1,i3,,
    E0,V0,u3,V1,i4,,
    E0,V0,u3,V1,i5,,
    E1,V0,u1,V1,i3,,
    E1,V0,u2,V1,i1,,
    E1,V0,u2,V1,i4,,
    E1,V0,u3,V1,i2,,
    E1,V0,u3,V1,i3,,
    E2,V1,i1,V2,t1,,
    E2,V1,i2,V2,t2,,
    E2,V1,i4,V2,t2,,
    E2,V1,i4,V2,t3,,
    E2,V1,i5,V2,t3,,

#### A second example

![logo](https://raw.githubusercontent.com/pedroramaciotti/HINPy/master/docs/example.png)

File available in *datasets* as `example.csv`:

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

#### Producing and evaluating recommendations

Upcoming section. You can take a peek in the *examples* folder.

#### Time series

Upcoming section.

#### Applications in other domains

Upcoming section.

