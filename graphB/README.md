[Data Lab @ TXST](DataLab12.github.io)

# graphB software 

## About 
name of the algorithm, **graphB** is short for **graph B**alancing. graphB implements algorithm that can run stand-alone or distributed to compute metrics for nodes and edges from graph frustration cloud, as outlined in this [paper](https://arxiv.org/abs/2009.07776).

### Faculty
* [Jelena Tešić](jtesic.github.io), Assistant Professor, Computer Science, Texas State University
* [Lucas Rusnak], Assistant Professor, Math, Texas State University

### Students
* Eric Hull, Joshua Mitchell 

## Abstract 
Attitudinal Network Graphs (ANG) are network graphs where edges capture an expressed opinion: two vertices connected by an edge can be agreeable (positive) or antagonistic (negative). Measure of consensus in attitudinal graph reflects how easy or difficult consensus can be reached that is acceptable by everyone. Frustration index is one such measure as it determines the distance of a network from a state of total structural balance. In this paper, we propose to measure the consensus in the graph by expanding the notion of frustration index to a frustration cloud, a collection of nearest balanced states for a given network. The frustration cloud resolves the consensus problem with minimal sentiment disruption, taking all possible consensus views over the entire network into consideration. A frustration cloud based approach removes the brittleness of traditional network graph analysis, as it allows one to examine the consensus on entire graph. A spanning-tree-based balancing algorithm captures the variations of balanced states and global consensus of the network, and enables us to measure vertex influence on consensus and strength of its expressed attitudes. The proposed algorithm provides a parsimonious account of the differences between strong and weak statuses and influences of a vertex in a large network, as demonstrated on sample attitudinal network graphs constructed from social and survey data. We show that the proposed method accurately models the alliance network, provides discriminant features for community discovery, successfully predicts administrator election outcome consistent with real election outcomes, and provides deeper analytic insights into ANG outcome analysis by pinpointing influential vertices and anomalous decisions.

## Implementation 

Python pipeline is designed to reuse existing computations (connected component, spanning trees, balancing results).  It consists of 3 steps: pre-process, process, and post-process. 
* graphB Implementation [notes](GRAPHB.md)

## Setup 

graphB should be cloned at the same level as sample data repository. 
*graphB setup [notes](SETUP.md)

In local directory <DIR>, check out 2 repositories: 
Checkout https://github.com/DataLab12/graphB

## Dry Run ##

1. Install Anaconda 

2. Open terminal in graphB repo (where it is locally):
```
>>cd <_DIR>/graphB/graphB
>>conda env create -f win_env.yml //if Windows
>>conda env create -f linux_env.yml //if Linux
>>conda activate cam
```
4. Setup configs folder (optional - currently set for data-test)
* copy folder **configs_template**, rename it to **configs** 
* repo data-highland_tribes should be at the same level at graphB/
* configs file options and hierarchy [explanation](configs_template/README.md)
```
>>python run.py
>>python run.py 0
```
5. Result Analysis 
* To view results go to data_highland-tribes/Output_Data/

[Data Lab @ TXST](DataLab12.github.io)
