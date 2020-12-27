## Detailed Setup

1. Install anaconda:  
```
>>[On Linux](https://docs.anaconda.com/anaconda/install/linux/)  
>>[On Windows](https://docs.anaconda.com/anaconda/install/windows/)  
```
2. Clone graphB repository 
```
   >>cd <DIR> 
   >>git clone https://github.com/DataLab12/graphB   
```  

3. Setup conda environments  

      Enter the following commands in terminal (linux) or in an anaconda prompt (windows):
```
      >> conda env create -f  conda_environments/win_env.yml // windows  
      >> conda env create -f conda_environments/linux_env.yml // linux  
      >> conda init --all   
      >> conda activate cam    
      >> pip install --ignore-installed pyyaml  
```    
      **Close the terminal to apply changes.**  
      
4. Setup config files
     * add .YAML file for each new dataset as explained [here](configs/README.md) 
```
      >> cd <DIR>/graphB/graphB/configs 
```      
 
5. Run the software  
``` 
      >> python run.py  
``` 
 * Terminal output will be available datasets to run on. These correlate to the config files in the configs folder.  
 * Once decided which dataset you want to run with config options in corresponding config file:  
      >> python run.py <i> (integer index from above terminal output)  
 
 * Status output is created in <DIR>/graphB/data-(name)/Output_Data/graphB directory. 
 * Timing files for various aspects of the software are created in <DIR>/graphB/data-(name)/Output_Data/Timing directory
 * Interim h5 files that the program uses to generate status output are kept in <DIR>/graphB/data-(name)/Data directory
 * Note: Spanning tree h5 files in Data directory are not overwritten when multiple runs are done. In order to get postprocessing results on only the trees you are currently running, old trees will need to be deleted or moved to a separate folder.
           
## Add New Dataset


*In config files there are three naming parameters:   
      * **dataset**   
      * **data_subset_type**  
      * **matrix_name**  
* These naming parameters map to the dataset repo and Input_Data, see data-test example:
  * dataset: [data-test](../data-test)
  * data_subset_type: 
```
A given datasets repo name is data-(dataset)  
Input_Data files are named as (data_subset_type)_(matrix_name)_edges.csv and (data_subset_type)_(matrix_name)_users.csv  
Names of config files correspond as well, i.e. (dataset)_(data_subset_type)_(matrix_name).yaml  
```      
**Example dataset and all of its members:**  
```
config file: test_highland_tribes.yaml  
parameters in config file: dataset: test, data_subset_type: highland, matrix_name: tribes  
path to Input_Data files: data-test/Input_Data/highland_tribes_edges.csv, data-test/Input_Data/highland_tribes_users.csv  
```      
**The software is configured this way to allow customization among many different subsets in one dataset.**

### Input_Data examples

* Input_Data folder should only contain edges and users csv files matching the naming format shown above.  
* edges files will contain comma separated triples of (from, to, edge weight)  
* users files will contain comma separated tuples of (numeric ID, string ID) or comma separated triples of (numeric ID, string ID, label) if the dataset has any type of labels to apply to the nodes in the network.  
* If the users are being assigned labels, it must be a label that can be represented in 1 bit binary. i.e. winning/losing, diagnosed/not diagnosed, sale completed/sale not completed, etc.  

*Example edges.csv file* 
```
From,To,Edge_Weight
0,1,1
0,3,-1
0,500,1
etc.
```
*Example users.csv file without labels*
```
Node_ID,User_ID
0,user0
1,user1
2,userName
etc.
```
*Example users.csv file with labels*
```
Node_ID,User_ID,Label
0,user0,1
1,user1,0
2,userName,1
etc.
```

### Data 

* All of the spanning tree h5 files will be sent to the Data folder in the associated dataset repository.
* An interim symmetric matrix file, 0.h5, is also saved in this directory and should not be deleted. This is what is created during the 'preprocess' step.
* The user can use the h5dump command if they wish to view the contents of any of these files.

### Output Data  

* For description of Output_Data/Timing files and timing results, click [here](TIMING.md)
* There will be 4 files written to the data-(dataset)/Output_Data/graphB/(data_subset_type)_(matrix_name)/ folder for each run.
* All names of files correspond to that specific run. Naming is as follows: (numOfTrees)(typeOfTrees)_(parallelism)_(weightedFlag)_(outcomesFlag)_(typeOfOutput).extension  
* Example filename: 10breadth_serial_unweighted_no_outcomes_status.csv
* Each parameter is described below:
```
numOfTrees: The number of trees set to generate in the config file when run was performed  
typeOfTrees: The type of spanning trees used in the graph balancing algorithm. options are breadth, depth, or random  
parallelism: Serial or Spark. Spark only works on TXState's LEAP HPC.  
weightedFlag: Should always be unweighted. This corresponds to a previous experiment when manipulating the status values due to certain criteria.  
outcomesFlag: Whether or not the users file had labels (aka outcomes)  
typeOfOutput: status, vertex_df, status_outliers
```  
* The status values are shown in csv and png form with the typeOfOutput flag: status  
* The outliers of the data are printed to a txt file with typeOfOutput flag: status_outliers
* The vertex df that is used to compute status values is saved in a pkl file with typeOfOutput flag: vertex_df
