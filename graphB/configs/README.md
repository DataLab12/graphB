# Config YAML files meaning 

* Select between 'spark', 'parallel', or 'serial'(default)
parallelism: 'serial' 

* Select between 'current'(default) or 'LEAP'
machine: 'current' 


## Preprocessing parameters (Raw Data --> Input Data)

* Would you like to make the Input Data again or for the first time? (i.e. full h5 matrix)
preprocess_again: Yes 

* Would you like to make the symmetricized h5? Note: If preprocess_again: Yes, then h5 is made automatically 
make_symm: Yes 

* Would you like to make the unsymmetricized h5? Note: If preprocess_again: Yes, then h5 is made automatically 
make_unsymm: Yes 

* Does this dataset have labels or colors for each vertex?
has_labels: No  

* What is the minimum number of vertices to consider making a full h5 matrix for? (Integer)
min_component_size: 2 

## Processing parameters "tree creation and balancing" (Input Data --> Data)

* How many trees to make? (Integer)
num_random_trees: 10 

* What is the project name? "EXAMPLE"(default)
dataset: "EXAMPLE" 

* What is the type of dataset? "regular"(default)  
data_subset_type: "regular" 

* What is the datasets identifier? "regular"(default)
matrix_name: "regular"

* What is the particular component of the graph to make trees? Components ordered by number of vertices descending 
# (i.e. 0 is the biggest component). If the matrix is one connected component, then put enter 0(default). (Integer)
component_no: 0 

## Postprocessing Parameters (Data --> Output Data)

* Would you like to perform postprocess? Yes(default) 
postprocess_again: Yes

* Would you like to make all dataframes, plots, tables? No(default)
all: No  

* Would you like to make all dataframes? No(default)
all_dfs: No

* Would you like to make all plots? No(default)
all_plots: No

* Would you like to make all tables? No(default)
all_tables: No 

* If all: No and all_dfs: No, then select dataframes to make?  
dataframes:
  vertex_df: Yes
  tree_df: Yes
  edge_sign_df: No
  tree_edge_df: No
  treewise_edge_prediction_df: No
  edgewise_edge_prediction_df: No
 
* If all: No and all_plots: No, then select plots to make?
plots: 
  tree_bias_vs_c0: Yes 
  vertex_status_vs_id: Yes
  histograms: Yes

* If all: No and all_tables: No, then select tables to make?
tables:
  vertex_table: Yes
  tree_table: Yes
  tree_corr_table: Yes

* Would you like to make stats? 
stats:
  BEC_histogram: No
