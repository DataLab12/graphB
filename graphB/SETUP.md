# SETUP
1. Install Anaconda 

2. Open terminal in graphB repo (where it is locally):
```
>>cd <_DIR>/graphB/src
>>conda env create -f win_env.yml //if Windows
>>conda env create -f linux_env.yml //if Linux
>>conda activate cam
```
4. Setup configs folder 

* repo [data-test](../data-test) should be at the same level as graphB code folder 
* configs file options and hierarchy [explanation](src/configs/README.md)
```
>>python run.py
```
* Output list provides **index** for each configuration file availiable.
* Reads YAML files in configs folder.  
* How to configure YAML files details [README](configs/README.md)
* Code can be split into preprocessing, processing, and post-processing step 
* Note: Each time you make spanning trees, they will be added to the previous trees made. They do not overide each other, only concatinate.

```
>>python run.py 0
```

5. Result Analysis 
* To view results go to data-test/Output_Data/
    

# INSTRUCTIONS 

## Data 

### Raw_Data

- The Raw_Data directory will primarily consist of two types of csv files.
- The users.csv file maps the Node_ID to the User_ID and may contain Labels. 
- The edges.csv file consists of three columns. "From_Node_ID", "To_Node_ID", "Edge_Weight"
- Note: No 0 Edge_Weight should be in edges.csv

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

### Input_Data   

  * Requires Raw_Data
  * Before any analysis can be done, the raw data (csv) has to be converted into its matrix h5 format. 
  * This is the Input Data step. For every connected component (CC) of your data above ~25 vertices, (ordered from highest to lowest, so 0.h5 is the highest CC of your data), there are two h5 files: 
  * The symmetricized matrix
  * The assymetric matrix.

  * The symmetric matrix will be used to generate trees and balanced matrices. 
  * The assymmetric matrix is used for degree analysis (i.e. in/out degree histograms) as part of Output Data.

### Data

 * Requires Input_Data
 * When we refer to Data, we specifically mean h5 files containing balanced versions of a data set as well as the trees used to do perform the specific balancing. 
 * Once this data is generated, the files will not be overwritten.


### Output_Data

  * Requires Data
  * Plots, dataframes, statistics, tables, etc. as a result of analyzing the Data

