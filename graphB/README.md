# About graphB

**graphB** algorithmm, short for **graph B**alancing, implements graph frustration cloud and resulting graph measures, as presented in this [paper](https://arxiv.org/abs/2009.07776).  


The graphB project is led by  Texas State faculty [Jelena Tešić](jtesic.github.io) and [Lucas Rusnak](https://www.math.txstate.edu/about/people/faculty/rusnak.html). First public release og graphB software was summer 2020 (ver 1.0 development led by graduate student [Joshua Mitchell](https://lelon.io/), and second and final release was Dec 2020, led by undergraduate student [Eric Hull](https://github.com/hullo-eric).  

Detailed setup and notes are in graphB [notebook](GRAPHB.md). 

Martin Burtscher's team scaled the discovery and balancing of fundamental cycles in 2020, and allowed us to extend the frustration cloud concept to larger social graphs, see new implementation [here](https://userweb.cs.txstate.edu/~burtscher/research/graphB/).



## Quick setup


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

2. Checkout https://github.com/DataLab12/graphB or pull the latest graphB version to local directory <DIR> .

   a. open terminal in graphB repo (where it is locally):
```
>>cd <DIR>/graphB/graphB
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
