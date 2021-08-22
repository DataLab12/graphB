## Timing Analysis of the Code

Detailed performance analysis of the code on several datasets [TIMING](TIMING.md)

## Implementation and Setup Notes 

1. Install Anaconda. Make sure all packages are installed.  If Anaconda is installed follow the steps below: 

    a. open terminal window as Admin (Windows) and make sure all file permissions are set by sudo on Linux.
	```
     >>cd <_DIR>/graphB
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
>>cd <_DIR>/graphB
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

# Dataset Notations, Format, and Example

| Example    | Figure     |  Data     |
| -----------| ---------- | --------- |
| Example 1A | ![Example 1A](figures/1A-signs.jpg) | [users](Input_Data/test1A_users.csv) and [edges](Input_Data/test1A_edges.csv) |
| Example 2A | ![Example 2A](figures/2A-signs.jpg) | [users](Input_Data/test2A_users.csv) and [edges](Input_Data/test2A_edges.csv) |

More reproducibility test data in [Input_Data](Input_Data/README.md) folder

## Input_Data format 

The Raw_Data directory will primarily consist of two types of csv files.
* The users.csv file maps the Node_ID to the User_ID and may contain Labels. 
* The edges.csv file consists of three columns. "From_Node_ID", "To_Node_ID", "Edge_Weight"
* Note: No 0 Edge_Weight should be in edges.csv

Underlining unsigned graph: ![Vertices](figures/Nodes.jpg) and ![Edges](figures/Edges.jpg)

name1_name2_users.csv example without labels:  
 ``` 
  Node ID,User ID
  0,R1
  1,R2
  2,R3
  ..
```
name1_name2_users.csv example with labels:  
```
  Node ID,User ID,Labels
  0,R1,1
  1,R2,0
  2,R3,1
  ...
```

name1_name2_edges.csv example:  
``` 
  From Node ID, To Node ID, Edge Weight
  0,1,-1
  0,2,-1
  1,2,1
  ...
```
name1_name2_edges.csv example from survey data:  
``` 
  From Node ID,To Node ID,Edge Weight,Rating
  0,1,-1,1
  0,2,-1,0
  1,2,1,5
  ...
```

## Data   

  * Before any analysis can be done, the raw data (csv) has to be converted into its matrix h5 format. 
  * For every connected component (CC) of your data above x vertices, (ordered from highest to lowest, so 0.h5 is the highest CC of your data), there are two h5 files: 
    * The symmetricized matrix - used for generate trees and balanced matrices. 
    * The assymetric matrix - used for degree analysis (i.e. in/out degree histograms) as part of Output Data.
   * Next, the code produces a set of h5 files containing balanced versions of a data set per spanning tree 
     * as well as the trees used to do perform the specific balancing. 
     * once this data is generated, the files will not be overwritten.


## Output_Data

  * Requires Data
  * Plots, dataframes, statistics, tables, etc. as a result of analyzing the Data
