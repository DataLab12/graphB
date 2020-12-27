# **github.com/DataLab12/graphB**

## Run grapB code 

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
``` 
      >> python run.py <i> (integer index from above terminal output)  
```

# graphB Data Science Pipeline 
           
## Add New Dataset

*In config files there are three naming parameters:  
      * <dataset>
      * <name1>   
      * <name2>  
* These naming parameters map to the dataset repo and Input_Data, see data-test example:

1. Name the dataset in form <name1>_<name2> e.g. higland_tribes 
  * <dataset>: test -> repo name is [data-test](../data-test)
  * <name1>: higland
  * <name2>: tribes 

2. Add <name1>_<name2>_edges.csv and <name1>_<name2>_users.csv to data-<dataset>/Input_Data

   [../data-test/Input_Data](../data-test/Input_Data) example
   * edges files example [highland_tribes_edges.csv](../data-test/Input_Data/highland_tribes_edges.csv)
   * user file example [highland_tribes_users.csv](../data-test/Input_Data/highland_tribes_users.csv)  

* edges files will contain comma separated triples of (from, to, edge weight)  
* users files will contain comma separated tuples of (numeric ID, string ID) or comma separated triples of (numeric ID, string ID, label) if the dataset has any type of labels to apply to the nodes in the network.  
* If the users are being assigned labels, it must be a label that can be represented in 1 bit binary. i.e. winning/losing, diagnosed/not diagnosed, sale completed/sale not completed, etc.  

*Example _edges.csv file* 
```
From,To,Edge_Weight
0,1,1
0,3,-1
0,500,1
etc.
```
*Example _users.csv file without labels*
```
Node_ID,User_ID
0,user0
1,user1
2,userName
etc.
```
*Example _users.csv file with labels*
```
Node_ID,User_ID,Label
0,user0,1
1,user1,0
2,userName,1
etc.
```

3. Add <dataset>_<name1>_<name2>.yaml file to [configs](configs/) folder 
  * use [test_higland_tribes.yaml](configs/test_highland_tribes.yaml) file as starting point 
  * detailed explanation of all fileds is [here](configs/README.md) 
  
## Pre-Processsing 
* Pre-processing step transforms data from Raw_Data to Input_Data folder of the collection: any input graph is transformed into (*_users.csv,*_edges.csv) file tuple 
   *  _edges.csv file as line entry of <from>, <to>, <vote>
   * corresponding _users.csv file that assigns all nodes unique IDs reflected in _edges file 
* Next step is the computation of largest connected component: 
   * the edges file is converted to .CSR matrix format, and then to NetworkX graph format using 
            ```networkx.from_scipy_sparse_matrix()``` 
   * This implementation of graphB ignores 0 edges, takes into account only positive or negative edges. 
   * Largest connected component of input graph is calculated using NetworkX method 
            ```networkx.connected_component_subgraphs()```
	 * Largest CC is then converted back to CSR format and written to 
	        ```Input_Data/*h5 networkx.to_scipy_sparse_matrix()```
			

## Processing 

### Data Folder 

* example: [../data-test/Data](../data-test/Data).
* contains intermediate processing steps
  * interim symmetric matrix file, 0.h5 for the dataset
  * spanning tree h5 files (all spanning and balancing trees from all runs if not deleted) 
  * use the h5dump to view content

### Tree Generation 

There are three different methods for tree generation. Trees can be generated and saved separately.
  ```Input_Data/*.h5``` is loaded back into NetworkX using ```networkx.from_scipy_sparse_matrix()```
1. **random spanning tree**: random weights are assigned to all of the edges; Kruskal’s algorithm is run on the random weighted graph
   ```networkx.minimum_spanning_tree()```, spanning tree generated from Kruskal’s is taken as a subgraph from the original graph to maintain the original weights using 
   ```networkx.edge_subgraph()```, 
   and tree is converted to NetworkX graph format and saved. 
2.  **breadth-first tree**: readth trees are made starting at highest degree node in the graph and then descending after,
	```scipy.sparse.csgraph.breadth_first_tree()```, and converted to NetworkX graph format
	```networkx.from_scipy_sparse_matrix()```
2. **depth-first tree**: depth trees are made starting at highest degree node in the graph and descending, usig
    ```scipy.sparse.csgraph.depth_first_tree()```, and and converted to NetworkX graph format
	```networkx.from_scipy_sparse_matrix()```

### Balancing Algorithm

For each tree, the algorithm finds all cycles in the graph that selected spanning trees forms with edges not in spanning tree.
* If the cycles have a product of -1, the edge sign (edge not in spanning tree) is changed.
* Result is balanced graph (each fundamental cycle in the graph is positive). 
* Negative edges are removed, and largest remaining connected component is found. 
* The information on node membership to largest cut, and change of sign of edge is saved as Data/*/*/*/*.h5 file 
  
The process is repeated for each sampled spanning tree 
  

## Post-Processing 

* Output_Data folder contains statistics computed from all sampled trees and resulted balanced states 
  * status is computed by counting the number of times the vertex was in largest connected component out of all the spanning trees/balanced graphs generated.

### Output_Data Folder 

1. [Output_Data/Timing](../data-test/Output_Data/Timing) has timing results for all data, see [details](TIMING.md).
2. [Output_Data/graphB/higland_tribes](../data-test/Output_Data/graphB/highland_tribes) contains results of code runs. 
 * All names of files correspond to specific run and parameter changes in config, e.g. <numOfTrees><typeOfTrees>_<parallelism>_<weightedFlag>_<outcomesFlag>_<typeOfOutput>.csv 
   * Example filename: 10breadth_serial_unweighted_no_outcomes_status.csv(.png)
   * numOfTrees: The number of trees set to generate in the config file when run was performed  
   * typeOfTrees: The type of spanning trees used in the graph balancing algorithm. options are breadth, depth, or random  
   * parallelism: Serial or Spark. Spark only works on TXState's LEAP HPC.  
   * weightedFlag: Should always be unweighted. This corresponds to a previous experiment when manipulating the status values due to certain criteria.  
   * outcomesFlag: Whether or not the users file had labels (aka outcomes)  
   * typeOfOutput: status, vertex_df, status_outliers
   * The status values are shown in csv and png form with the typeOfOutput flag: status  
   * The outliers of the data are printed to a txt file with typeOfOutput flag: status_outliers
   * The vertex df that is used to compute status values is saved in a pkl file with typeOfOutput flag: vertex_df


  
 