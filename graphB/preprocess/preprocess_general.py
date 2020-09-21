import numpy as np
from scipy.sparse import csgraph
import pickle
import h5py
import os
import sys
import subprocess
import yaml
import csv

import networkx as nx
from datetime import datetime

from collections import Counter
from os.path import abspath, dirname, isfile

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from preprocess.matrix_loader import get_full_unsym_csr_adj_matrix_and_possibly_outcomes_from_csv
from dataset_paths import get_full_sym_h5_path, get_full_unsym_h5_path
from constants import CONFIG_BASE

# Called in Matrix creation 
def get_yaml_config_obj_by_key_tuple(dataset, data_subset_type, matrix_name, component_no):
	# Example parameter set: "example1", "regular", "regular", "0" (or 0, maybe)
	config_path = CONFIG_BASE + dataset + "/" + data_subset_type + "/" + matrix_name + "/" + str(component_no) + ".yaml"
	config_obj = None
	with open(config_path, 'r') as stream:
	    try:
	    	config_obj = yaml.load(stream)
	    except yaml.YAMLError as exc:
	    	print(exc)
	return config_obj

# Called in preprocess_locally 
def full_h5_exists(config_obj, is_symmetric):
  h5_path = None
  if is_symmetric:
    h5_path = get_full_sym_h5_path(config_obj)
  else:
    h5_path = get_full_unsym_h5_path(config_obj)
  return isfile(h5_path + "0.h5") 

# Called in create_full_h5 
def order_components_descending(labels):
    comp_labels, counts = np.unique(labels, return_counts=True)
    dict_hist = dict(zip(comp_labels, counts))
    sorted_keys_list = sorted(dict_hist, key=dict_hist.get, reverse=True)
    labels = [sorted_keys_list.index(element) for element in labels]
    return labels

# Called in preprocess_Locally 
def create_full_h5(config_obj, is_symmetric):
  csr_adj_matrix, users = get_full_unsym_csr_adj_matrix_and_possibly_outcomes_from_csv(config_obj)
  print("Got full adj matrix (and possibly outcomes).")
  if is_symmetric:

    G_pre_symm = nx.from_scipy_sparse_matrix(csr_adj_matrix)
    csr_adj_matrix = symmetricize(csr_adj_matrix)
    set_all_diag_to_zero(csr_adj_matrix)
    print("Symmetricized.")

    num_connected_components, labels = csgraph.connected_components(csr_adj_matrix, return_labels=True) # returns a list of the connected components with each one given a label. i.e. 0,1,2, etc.
    print("num cc: ", num_connected_components)
    print("labels: ", labels)
    G = nx.from_scipy_sparse_matrix(csr_adj_matrix)
    connected_comps = [c for c in sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)]
    print("Got the connected components.")
    comp_labels, counts = np.unique(labels, return_counts=True)
    print("comp labels: ", comp_labels)
    print("counts: ", counts)
    dict_hist = dict(zip(comp_labels, counts))
    labels = order_components_descending(labels)
    comp_labels, counts = np.unique(labels, return_counts=True)
    dict_hist = dict(zip(comp_labels, counts))
    
    for i in range(num_connected_components):
      if dict_hist[i] < config_obj['min_component_size']:
        break
      else: 
        print("Writing component ", i)
        write_full_h5(connected_comps[i], config_obj, i, is_symmetric, labels, users)
### This was originially supposed to work with the config option 'is_symmetric' being set to 'No' but 
### upon inspection I found that that option does not work at all so I have it disabled. - Eric
#  else:
#    write_full_h5(csr_adj_matrix, config_obj, None, is_symmetric, None, users)

# Called in write_full_h5
def get_neighbors(vertex_number, graph_adj_matrix):
  neighbors = []
  if isinstance(graph_adj_matrix, np.ndarray):
      neighbors = [index for index, adjacency in enumerate(graph_adj_matrix[vertex_number]) if adjacency != 0]
  else:
      neighbors = list(np.split(graph_adj_matrix.indices, graph_adj_matrix.indptr)[vertex_number + 1:vertex_number + 2][0]) # gets a list of neighbors of vertex <vertex_number>
  return neighbors

# called in create_full_h5
def write_full_h5(nx_connected_comp_graph, config_obj, component_no, is_symmetric, labels, users):
  map_to_node_id = None
  if labels:
      map_to_node_id = [index for index, element in enumerate(labels) if int(element) == component_no]
      component_no = int(component_no)
  else:
      map_to_node_id = [i for i in range(csr_adj_matrix.shape[0])]
      component_no = "full"
  full_h5_path = None
  if is_symmetric:
    full_h5_path = get_full_sym_h5_path(config_obj, True)
  else:
    full_h5_path = get_full_unsym_h5_path(config_obj, True)

  create_if_not_exists(full_h5_path)
  try:
    f = h5py.File(full_h5_path + str(component_no)+ ".h5", 'w')
    csr_adj_matrix = nx.to_scipy_sparse_matrix(nx_connected_comp_graph, nodelist = map_to_node_id)
    create_matrix_h5_file(f, csr_adj_matrix)
    f.attrs['dataset'] = config_obj['dataset']
    f.attrs['data_subset_type'] = config_obj['data_subset_type']
    f.attrs['matrix_name'] = config_obj['matrix_name']
    f.attrs['component_no'] = component_no
    num_vertices = csr_adj_matrix.shape[0]
    grp = f.create_group('full_neighbors_list')
    progress_indicator = int(num_vertices / 20)

    print("Getting neighbors list.")
    start_neighbors = datetime.now()
    for i in range(num_vertices):
      if progress_indicator != 0 and num_vertices % progress_indicator == 0:
        print("Percent done: ", (i / num_vertices) * 100)
      grp.create_dataset(str(i), data=get_neighbors(i, csr_adj_matrix))
    print('Neighbors List Acquired, took: (hh:mm:ss.ms) {}'.format(datetime.now() - start_neighbors))
   ### I used this block when debugging the node mapping edges issue, left in in case the code is useful later.
   ### - Eric
   # graph = csr_adj_matrix.toarray()
   # with open('TestP1_wiki_edges_test.csv', 'w') as writefile:
   #     writer = csv.writer(writefile)
   #     writer.writerow(['from', 'to', 'weight'])
   #     for (m, n), value in np.ndenumerate(graph):
   #          if value != 0:
   #              writer.writerow([map_to_node_id[m], map_to_node_id[n], value])

    f.create_dataset('mapping_to_original', data = map_to_node_id)
   
    node_ids_subset = users[['Node ID']]
    user_ids_subset = users[['User ID']]
    node_ids = [x for x in node_ids_subset.values]
    user_ids = [x for x in user_ids_subset.values]
    f.create_dataset('node_ids', data = node_ids)
    
    dt = h5py.special_dtype(vlen=str)
    ds = f.create_dataset('user_ids', (len(user_ids),), dtype=dt)
    for i in range(len(user_ids)):
      ds[i] = user_ids[i]
    
    if len(users.columns) > 2 and users.columns[2] == 'Label':
        create_outcomes_map(users, f, map_to_node_id)

    f.attrs['is_symmetric'] = is_symmetric
  finally:
    f.close()
  print("Saved full h5: ", "(", config_obj['dataset'], ", ", config_obj['data_subset_type'], ", ", config_obj['matrix_name'], ", ", component_no, ") - symmetric: ", is_symmetric)
  print("to: ", full_h5_path)

def create_outcomes_map(users, h5_file, map_to_node_id):
    f = h5_file
    users_dict = dict()
    outcomes_map = list()
   
    user_nodes = list(users["Node ID"])
    user_labels = list(users['Label'])
    
    for item in range(len(user_nodes)):
      users_dict.setdefault(user_nodes[item], user_labels[item])
         
    for key in map_to_node_id:
      if key in users_dict:
        outcomes_map.append(users_dict[key])
     
    f.create_dataset('outcomes', data = outcomes_map)
    

# Called in Matrix creation 
def preprocess_locally(config_obj):
  print("Preprocessing on: ", config_obj['machine'])
  if config_obj['make_symm'] and ((full_h5_exists(config_obj, True) and config_obj['preprocess_again']) or not (full_h5_exists(config_obj, True))):
    # if making it is requested AND it doesn't exist or it exists but we want it remade, then make it
    print("Making a symmetric full H5.")
    create_full_h5(config_obj, True)
  else:
    print("Not making a symmetric full H5.")
  print("---------- Done making symmetric full H5 (if one was made)")
  if config_obj['make_unsymm'] and ((full_h5_exists(config_obj, False) and config_obj['preprocess_again']) or not (full_h5_exists(config_obj, False))):
    # if making it is requested AND it doesn't exist or it exists but we want it remade, then make it
    print("Making an assymmetric full H5.")
    create_full_h5(config_obj, False)
  else:
    print("Not making an asymmetric full H5.")
  print("---------- Done making assymmetric full H5 (if one was made)")
  return 0
  
# Not called by any other function locally 	
def submit_preprocess_LEAP_job(config_obj):
  print("Submitting preprocess job on LEAP")
  # retrieve (dataset, data_subset_type, matrix_name, component_no) from config_obj
  dataset = config_obj['dataset']
  data_subset_type = config_obj['data_subset_type']
  matrix_name = config_obj['matrix_name']
  component_no = config_obj['component_no']
  # then call a bash script that calls preprocess_general with those parameters
  # subprocess.check_call("preprocess_general.sh %s %s %s %s" % (dataset, data_subset_type, matrix_name, str(component_no)))
  LEAP_output = subprocess.run(['preprocess/wrapper_preprocess_general.sh', dataset, data_subset_type, matrix_name, str(component_no)], stdout=subprocess.PIPE).stdout.decode('utf-8')
  print("LEAP Output: ", LEAP_output)
  job_ID = int(LEAP_output.split()[-1])
  print("subprocess output: ", LEAP_output)
  return job_ID

# Called in write_full_h5
def create_matrix_h5_file(g, csr_m):  
    g.create_dataset('data', data = csr_m.data)
    g.create_dataset('indptr', data = csr_m.indptr)
    g.create_dataset('indices', data = csr_m.indices)
    g.attrs['shape'] = csr_m.shape

# Called by write_full_h5
def create_if_not_exists(directory_to_possibly_create):
  if not os.path.exists(directory_to_possibly_create):
    os.makedirs(directory_to_possibly_create)


# Called in create_full_h5
def symmetricize(data_matrix):
  if (data_matrix != data_matrix.transpose()).nnz > 0: # data matrix is not symmetric
      data_matrix = (data_matrix + data_matrix.transpose()).sign()
  return data_matrix

# Called in create_full_h5
def set_all_diag_to_zero(csr_m):
  csr_m.setdiag(0)

def save_obj(obj, name):
    with open('Preprocessed_Data/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('Preprocessed_Data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


#############################################
### MATRIX CREATION DICTIONARY
#############################################

if __name__ == "__main__":
  print("Running preprocess main with args: ", sys.argv)
  dataset = str(sys.argv[1])
  data_subset_type = str(sys.argv[2])
  matrix_name = str(sys.argv[3])
  component_no = int(sys.argv[4])
  config_obj = get_yaml_config_obj_by_key_tuple(dataset, data_subset_type, matrix_name, component_no)
  preprocess_locally(config_obj)
