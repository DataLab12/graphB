# graphB software 

## About 
**graphB** is short for **graph B**alancing. graphB implements algorithm that can run stand-alone or distributed to compute metrics for nodes and edges from graph frustration cloud, as outlined in this [paper](https://arxiv.org/abs/2009.07776).

* faculty: Lucas Rusnak, Math and [Jelena Tešić](jtesic.github.io], Computer Science
* current students: Eric Hull, Maria Tomasso, Blane Rhodes
* former students: Joshua Mitchell, Connie Angeley, Benjamin Bond

## Abstract 
Attitudinal Network Graphs (ANG) are network graphs where edges capture an expressed opinion: two vertices connected by an edge can be agreeable (positive) or antagonistic (negative). Measure of consensus in attitudinal graph reflects how easy or difficult consensus can be reached that is acceptable by everyone. Frustration index is one such measure as it determines the distance of a network from a state of total structural balance. In this paper, we propose to measure the consensus in the graph by expanding the notion of frustration index to a frustration cloud, a collection of nearest balanced states for a given network. The frustration cloud resolves the consensus problem with minimal sentiment disruption, taking all possible consensus views over the entire network into consideration. A frustration cloud based approach removes the brittleness of traditional network graph analysis, as it allows one to examine the consensus on entire graph. A spanning-tree-based balancing algorithm captures the variations of balanced states and global consensus of the network, and enables us to measure vertex influence on consensus and strength of its expressed attitudes. The proposed algorithm provides a parsimonious account of the differences between strong and weak statuses and influences of a vertex in a large network, as demonstrated on sample attitudinal network graphs constructed from social and survey data. We show that the proposed method accurately models the alliance network, provides discriminant features for community discovery, successfully predicts administrator election outcome consistent with real election outcomes, and provides deeper analytic insights into ANG outcome analysis by pinpointing influential vertices and anomalous decisions.

## Implementation and Setup 

Python pipeline is designed to reuse existing computations (connected component, spanning trees, balancing results).  It consists of 3 steps: pre-process, process, and post-process. 
  * graphB introduction and dry run [notes](README.md)
  * graphB Implementation [notes](graphB/README.md)
  * graphB Setup [notes](graphB/SETUP.md)


## Dry Run ##

1. Install Anaconda 

2. Open terminal in graphB repo (where it is locally):
```
>>cd <_DIR>/graphB/src
>>conda env create -f win_env.yml //if Windows
>>conda env create -f linux_env.yml //if Linux
>>conda activate cam
```
4. Setup configs folder 

* repo [data-test](data-test) should be at the same level as src folder in graphB 
* configs file options and hierarchy [explanation](src/configs/README.md)
```
>>python run.py
>>python run.py 0
```
5. Result Analysis 
* To view results go to data-test/Output_Data/
