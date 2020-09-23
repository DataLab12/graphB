#**DataLab12.github.io/graphB**

## History 
The project and collaboration of Jelena Tešić and Lucas Rusnak started in November 2017 and graphB code was a result of multiple contributions from [Data Lab](DataLab12.github.io) current, and former students.  
* Joshua Mitchell, Master student at Texas State led the initial graphB implementation, graphB 1.0.
* Eric Hull, undergraduate researcher led the subconsequent improvements for this graphB 2.0 release
* significant contributions to the code improvement were made by Ryan Zamora, Maria Tomasso, Benjamin Bond, and Connie Angeley 

# Implementation Notes 
Python pipeline is designed to reuse existing computations (connected component, spanning trees, balancing results).  It consists of 3 steps: pre-process, process, and post-process 

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
 