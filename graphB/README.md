
# graphB

**graphB** algorithmm, short for **graph B**alancing, implements graph frustration cloud and resulting graph measures, as presented in this [paper](https://arxiv.org/abs/2009.07776).

Data science pipeline consists of three steps: pre-process, process, and post-process, as explained in graphB [notes](GRAPHB.md). Detailed *setup* [notes](SETUP.md) 


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
