#  Automated run on sample data 
	```
     >>source [testRun.sh](testRun.sh]	 
	```
   * The example is set to run 10 trees, 1000 trees from the paper would take too long.
   
## [Docker image of the test run](https://hub.docker.com/repository/docker/jtesic/graph_balancing)
   
   1. Install [Docker](https://docs.docker.com/get-docker/)
   2. In terminal: 
   ```
   >>docker pull jtesic/graph_balancing:latest
   >>docker run latest
   ```
   * To build docker image in current folder
   ```
   >>docker build -t latest .
   >>docker run latest
   >>docker tag latest <USERNAME>/<REPO>:latest
   >>docker push <USERNAME>/<REPO>:latest
   ```
  
# graphB 

**graphB** algorithmm, short for **graph B**alancing, implements graph frustration cloud and resulting graph measures, as presented in this [paper](https://arxiv.org/abs/2009.07776).  

The graphB project is led by  Texas State faculty [Jelena Tešić](jtesic.github.io) and [Lucas Rusnak](https://www.math.txstate.edu/about/people/faculty/rusnak.html). First public release og graphB software was summer 2020 (ver 1.0 development led by graduate student [Joshua Mitchell](https://lelon.io/), and second release was Dec 2020, led by undergraduate student [Eric Hull](https://github.com/hullo-eric).  
* Timing Analysis [experiment](graphB/TIMING.md)
* graphB [notebook](graphB/GRAPHB.md) contains detailed setup and run steps 

* Martin Burtscher's team scaled the discovery and balancing of fundamental cycles in 2021, and allowed us to extend the frustration cloud concept to larger social graphs, see new implementation [here](https://userweb.cs.txstate.edu/~burtscher/research/graphB/).

# Timing Analysis 

  * [Detailed timing experiment](data-test/TIMING.md)
  * [Data Format and code run](data-test/README.md)

## Characterizing Attitudinal Network Graphs through Frustration Cloud


**Abstract** Attitudinal Network Graphs (ANG) are network graphs where edges capture an expressed opinion: two vertices connected by an edge can be agreeable (positive) or antagonistic (negative). Measure of consensus in attitudinal graph reflects how easy or difficult consensus can be reached that is acceptable by everyone. Frustration index is one such measure as it determines the distance of a network from a state of total structural balance. In this paper, we propose to measure the consensus in the graph by expanding the notion of frustration index to a frustration cloud, a collection of nearest balanced states for a given network. The frustration cloud resolves the consensus problem with minimal sentiment disruption, taking all possible consensus views over the entire network into consideration. A frustration cloud based approach removes the brittleness of traditional network graph analysis, as it allows one to examine the consensus on entire graph. A spanning-tree-based balancing algorithm captures the variations of balanced states and global consensus of the network, and enables us to measure vertex influence on consensus and strength of its expressed attitudes. The proposed algorithm provides a parsimonious account of the differences between strong and weak statuses and influences of a vertex in a large network, as demonstrated on sample attitudinal network graphs constructed from social and survey data. We show that the proposed method accurately models the alliance network, provides discriminant features for community discovery, successfully predicts administrator election outcome consistent with real election outcomes, and provides deeper analytic insights into ANG outcome analysis by pinpointing influential vertices and anomalous decisions.  [arXiv](https://arxiv.org/abs/2009.07776).


[Data Lab @ TXST](DataLab12.github.io)
