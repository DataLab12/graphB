# About graphB

**graphB** algorithmm, short for **graph B**alancing, implements graph frustration cloud and resulting graph measures, as presented in this [paper](https://arxiv.org/abs/2009.07776).  


The graphB project is led by  Texas State faculty [Jelena Tešić](jtesic.github.io) and [Lucas Rusnak](https://www.math.txstate.edu/about/people/faculty/rusnak.html). First public release og graphB software was summer 2020 (ver 1.0 development led by graduate student [Joshua Mitchell](https://lelon.io/), and second and final release was Dec 2020, led by undergraduate student [Eric Hull](https://github.com/hullo-eric).  

Detailed setup and notes are in graphB [notebook](GRAPHB.md). 

Martin Burtscher's team scaled the discovery and balancing of fundamental cycles in 2020, and allowed us to extend the frustration cloud concept to larger social graphs, see new implementation [here](https://userweb.cs.txstate.edu/~burtscher/research/graphB/).



## Quick setup

1. Checkout https://github.com/DataLab12/graphB to local directory <DIR>

2. Install Anaconda 

3. Open terminal in graphB repo (where it is locally):
```
>>cd <_DIR>/graphB/graphB
>>conda env create -f win_env.yml //if Windows
>>conda env create -f linux_env.yml //if Linux
>>conda activate cam
```
4. (Optional) Add .yaml file for your dataset to configs folder 

5. Run the following code
```
>>python run.py
>>python run.py 0
```
6. See Results in
 ../data-test/Output_Data/

[Data Lab @ TXST](DataLab12.github.io)
