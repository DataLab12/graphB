#  Do a testRun to make sure it all works, then do a run on the data from the paper 
	```
     >>source testRun.sh
     >>source testRun.sh 	 
	```
   The example is set to run 10 trees, 1000 trees from the paper would take too long 

# graphB 

**graphB** algorithmm, short for **graph B**alancing, implements graph frustration cloud and resulting graph measures, as presented in this [paper](https://arxiv.org/abs/2009.07776).  

The graphB project is led by  Texas State faculty [Jelena Tešić](jtesic.github.io) and [Lucas Rusnak](https://www.math.txstate.edu/about/people/faculty/rusnak.html). First public release og graphB software was summer 2020 (ver 1.0 development led by graduate student [Joshua Mitchell](https://lelon.io/), and second release was Dec 2020, led by undergraduate student [Eric Hull](https://github.com/hullo-eric).  
* Timing Analysis [experiment](graphB/TIMING.md)
* graphB [notebook](graphB/GRAPHB.md) contains detailed setup and run steps 

* Martin Burtscher's team scaled the discovery and balancing of fundamental cycles in 2021, and allowed us to extend the frustration cloud concept to larger social graphs, see new implementation [here](https://userweb.cs.txstate.edu/~burtscher/research/graphB/).


## Characterizing Attitudinal Network Graphs through Frustration Cloud


**Abstract** Attitudinal Network Graphs (ANG) are network graphs where edges capture an expressed opinion: two vertices connected by an edge can be agreeable (positive) or antagonistic (negative). Measure of consensus in attitudinal graph reflects how easy or difficult consensus can be reached that is acceptable by everyone. Frustration index is one such measure as it determines the distance of a network from a state of total structural balance. In this paper, we propose to measure the consensus in the graph by expanding the notion of frustration index to a frustration cloud, a collection of nearest balanced states for a given network. The frustration cloud resolves the consensus problem with minimal sentiment disruption, taking all possible consensus views over the entire network into consideration. A frustration cloud based approach removes the brittleness of traditional network graph analysis, as it allows one to examine the consensus on entire graph. A spanning-tree-based balancing algorithm captures the variations of balanced states and global consensus of the network, and enables us to measure vertex influence on consensus and strength of its expressed attitudes. The proposed algorithm provides a parsimonious account of the differences between strong and weak statuses and influences of a vertex in a large network, as demonstrated on sample attitudinal network graphs constructed from social and survey data. We show that the proposed method accurately models the alliance network, provides discriminant features for community discovery, successfully predicts administrator election outcome consistent with real election outcomes, and provides deeper analytic insights into ANG outcome analysis by pinpointing influential vertices and anomalous decisions.  [arXiv](https://arxiv.org/abs/2009.07776).


## Timing Analysis of the Code

Detailed performance analysis of the code on several datasets [TIMING](TIMING.md)

## Implementation and Setup Notes 

1. Install Anaconda. Make sure all packages are installed.  If Anaconda is installed follow the steps below: 

    a. open terminal window as Admin (Windows) and make sure all file permissions are set by sudo on Linux.
	```
     >>conda update -n base -c defaults conda 
	```
    b. remove old packages and tarballs
	```
    >>conda  clean -p -t
	```
    c. remove old environments
	```
    >>conda env list
    >>conda env remove –name cam 
	```

2. Pull latest graphB from github.com/DataLab12/graphB and follow instructions. 

   a. open terminal in graphB repo (where it is locally):
```
>>cd <_DIR>/graphB/graphB
```
   b. Based on OS, create new environment 
```
>>conda env create -f env/win_env.yml //if Windows
```
or 
```
>>conda env create -f env/linux_env.yml //if Linux
```
or 
```
>>conda env create -f env/mac_env.yml //if Linux
```
make sure all the packages are installed. If succesfull, this is the terminal output:
```
done
#
# To activate this environment, use
#
#     $ conda activate graphB
#
# To deactivate an active environment, use
#
#     $ conda deactivate
>> conda activate graphB
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
* To view results go to [data-test/Output_Data/](data-test/Output_Data/) folder. 

[Data Lab @ TXST](DataLab12.github.io)
