# graphB 

**graphB** algorithmm, short for **graph B**alancing, implements graph frustration cloud and resulting graph measures, as presented in this [paper](https://arxiv.org/abs/2009.07776).  

The graphB project is led by  Texas State faculty [Jelena Tešić](jtesic.github.io) and [Lucas Rusnak](https://www.math.txstate.edu/about/people/faculty/rusnak.html). First public release og graphB software was summer 2020 (ver 1.0 development led by graduate student [Joshua Mitchell](https://lelon.io/), and second release was Dec 2020, led by undergraduate student [Eric Hull](https://github.com/hullo-eric).  
* Timing Analysis [experiment](TIMING.md)
* graphB [notebook](GRAPHB.md) contains detailed setup and run steps 

* Martin Burtscher's team scaled the discovery and balancing of fundamental cycles in 2020, and allowed us to extend the frustration cloud concept to larger social graphs, see new implementation [here](https://userweb.cs.txstate.edu/~burtscher/research/graphB/).


## Characterizing Attitudinal Network Graphs through Frustration Cloud


**Abstract** Attitudinal Network Graphs (ANG) are network graphs where edges capture an expressed opinion: two vertices connected by an edge can be agreeable (positive) or antagonistic (negative). Measure of consensus in attitudinal graph reflects how easy or difficult consensus can be reached that is acceptable by everyone. Frustration index is one such measure as it determines the distance of a network from a state of total structural balance. In this paper, we propose to measure the consensus in the graph by expanding the notion of frustration index to a frustration cloud, a collection of nearest balanced states for a given network. The frustration cloud resolves the consensus problem with minimal sentiment disruption, taking all possible consensus views over the entire network into consideration. A frustration cloud based approach removes the brittleness of traditional network graph analysis, as it allows one to examine the consensus on entire graph. A spanning-tree-based balancing algorithm captures the variations of balanced states and global consensus of the network, and enables us to measure vertex influence on consensus and strength of its expressed attitudes. The proposed algorithm provides a parsimonious account of the differences between strong and weak statuses and influences of a vertex in a large network, as demonstrated on sample attitudinal network graphs constructed from social and survey data. We show that the proposed method accurately models the alliance network, provides discriminant features for community discovery, successfully predicts administrator election outcome consistent with real election outcomes, and provides deeper analytic insights into ANG outcome analysis by pinpointing influential vertices and anomalous decisions.  [arXiv](https://arxiv.org/abs/2009.07776).

## Implementation and Setup Notes 

Python pipeline is designed to reuse existing computations (connected component, spanning trees, balancing results).  It consists of 3 steps: pre-process, process, and post-process, see [notes](GRAPHB.md)

1. In local directory <DIR>, check out 2 repositories: 
Checkout https://github.com/DataLab12/graphB

2. Install Anaconda 

3. Open terminal in graphB repo (where it is locally):
```
>>cd <_DIR>/graphB/graphB
>>conda env create -f env/win_env.yml //if Windows
>>conda env create -f env/linux_env.yml //if Linux
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
