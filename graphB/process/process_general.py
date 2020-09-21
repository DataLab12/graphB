import csv
import uuid
import subprocess
import h5py
import statistics
import sys
import yaml
import os
import gc
import pickle 

import networkx as nx
import numpy as np
import pandas as pd

from datetime import datetime
from joblib import Parallel, delayed # os.system("pip install joblib") if joblib isn't installed
from scipy.sparse import csgraph, csr_matrix
from numpy import prod

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from dataset_paths import get_full_sym_h5_path, get_balanced_h5_path, get_config_path, get_full_csr_adj

# Called in if statement 
def get_yaml_config_obj_by_key_tuple(dataset, data_subset_type, matrix_name, component_no):
	# Example parameter set: "example1", "regular", "regular", "0" (or 0, maybe)
    config_path = get_config_path(dataset, data_subset_type, matrix_name, component_no)
    print("config_path: ", config_path)
    config_obj = None
    with open(config_path, 'r') as stream:
	    try:
	    	config_obj = yaml.load(stream)
	    except yaml.YAMLError as exc:
	    	print(exc)
    return config_obj

##########################################################################################
			    ########## Graph Balancing ##########
##########################################################################################


#called in get_spanning_tree
def get_depth_first_tree(csr_adj_matrix, node_index):
    original_adj_graph = nx.from_scipy_sparse_matrix(csr_adj_matrix)
    degree_list = sorted([(degree, node) for node, degree in original_adj_graph.degree()], reverse = True)
    start_node = degree_list[node_index]
    start_node = start_node[1]
    print("start node is: ", start_node)
    depth_tree = csgraph.depth_first_tree(csr_adj_matrix, start_node) #makes a tree from depth first search
    return depth_tree

# Called in get_spanning_tree
def get_breadth_first_tree(csr_adj_matrix, node_index):
    original_adj_graph = nx.from_scipy_sparse_matrix(csr_adj_matrix)
    degree_list = sorted([(degree, node) for node, degree in original_adj_graph.degree()], reverse = True)
    start_node = degree_list[node_index]
    start_node = start_node[1]  
    breadth_tree = csgraph.breadth_first_tree(csr_adj_matrix, start_node) #makes a tree from breadth first search
    return breadth_tree

# Called in get_spanning_tree
def get_random_MST_adj_matrix(csr_adj_matrix, rand_weights):
    original_adj_graph = nx.from_scipy_sparse_matrix(csr_adj_matrix)
    i = 0
    ### These for loops iterate through each edge pair, if the first node in the pair
    ### is greater than the second node, a float value between 0 and 1 is assigned
    ### as the weight for that edge.
    for node, neighbors in original_adj_graph.adj.items():
        for neighbor, weight in neighbors.items(): 
            if node > neighbor:
                weight['weight'] = rand_weights[i]
                i += 1
    tree_rand_weights = nx.minimum_spanning_tree(original_adj_graph) # default is kruskal's
    rand_weight_tree_edges = tree_rand_weights.edges() 
    original_adj_graph_copy = nx.from_scipy_sparse_matrix(csr_adj_matrix)
    rand_MST = original_adj_graph_copy.edge_subgraph(rand_weight_tree_edges)
    csr_tree_adj = nx.to_scipy_sparse_matrix(rand_MST)
    return csr_tree_adj

# Called in get_spanning_tree
def get_random_st_adj_matrix(csr_adj_matrix, config_obj): # doesn't work yet
    NUM_VERTICES = csr_adj_matrix.shape[0]
    starting_vertex = random.randint(0, NUM_VERTICES - 1)
    visited = set([starting_vertex])
    unvisited = set([i for i in range(NUM_VERTICES)])
    unvisited.remove(starting_vertex)
    
    dok_st_adj_matrix = dok_matrix((NUM_VERTICES, NUM_VERTICES), dtype=int) # create adj matrix of same size as graph
    
    assert(csgraph.connected_components(csr_adj_matrix, return_labels=False) == 1)

    while len(visited) < NUM_VERTICES:
        # get a random edge from the visited set to the unvisited set
        outside_edge = self.get_connecting_edge(visited, unvisited, neighbors_dict)
        visited.add(outside_edge[1])
        unvisited.remove(outside_edge[1])
        dok_st_adj_matrix[outside_edge[1], outside_edge[0]] = csr_adj_matrix[outside_edge[1], outside_edge[0]]
        dok_st_adj_matrix[outside_edge[0], outside_edge[1]] = csr_adj_matrix[outside_edge[0], outside_edge[1]]

    return csr_matrix(dok_st_adj_matrix)

# Called in balance_graph
def get_spanning_tree(unbalanced_csr_adj_matrix, spanning_tree_type, tree_name, rand_weights, node_index):
    if spanning_tree_type == "random_MST":
        tree = None
        if hasattr(unbalanced_csr_adj_matrix, 'value'):
            tree = get_random_MST_adj_matrix(unbalanced_csr_adj_matrix.value, rand_weights[tree_name])
        else:
            tree = get_random_MST_adj_matrix(unbalanced_csr_adj_matrix, rand_weights[tree_name])
        nx_st_graph = nx.from_scipy_sparse_matrix(tree)
        assert(nx.is_tree(nx_st_graph))
        return tree
    elif spanning_tree_type == "random": ## This type is broken
        tree = get_random_st_adj_matrix(unbalanced_csr_adj_matrix)
        nx_st_graph = nx.from_scipy_sparse_matrix(tree)
        assert(nx.is_tree(nx_st_graph))
        return tree
    elif spanning_tree_type == 'breadth':
        tree = get_breadth_first_tree(unbalanced_csr_adj_matrix, node_index)
        nx_st_graph = nx.from_scipy_sparse_matrix(tree)
        assert(nx.is_tree(nx_st_graph))
        return tree
    elif spanning_tree_type == 'depth':
        tree = get_depth_first_tree(unbalanced_csr_adj_matrix, node_index)
        nx_st_graph = nx.from_scipy_sparse_matrix(tree)
        assert(nx.is_tree(nx_st_graph))
        return tree
    else:
        return None # could implement fake boss options here, not super high on priority list

# Called in get_unique_paths
def search_children(G, previous, current, path_dict, current_path):
    new_path = current_path + [current]
    if current in path_dict and len(current_path) > 0:
        for key in path_dict[current]:
            path_dict[current][key] = new_path 
    nbrs = neighbors(G, current, previous)
    if len(nbrs) > 0:
        nbrs = neighbors(G, current, previous)
        for child in nbrs:
            search_children(G, current, child, path_dict, new_path)  

# Called in search_children, get_neighbors, get_unvisited_neighbors, assign_component_numbers	
def neighbors(G, current, parent):
    neighbors_of_current = set(G[current])
    if type(parent) == int or type(parent) == np.int64 or parent is not None:
        return neighbors_of_current - set([parent])
    else:
        return neighbors_of_current

# Called in get_unique_paths
def create_edge_path_dict(path_dict):
    # returns a list of key value pairs: (v1, v2) --> path from v1 to v2, where v1 < v2
    edge_path_dict = {}
    for v1, v2 in [(v1, v2) for v1 in path_dict for v2 in path_dict if (v1 < v2 and v2 in path_dict[v1])]:
        edge_path_dict[(v1, v2)] = join_paths(path_dict, v1, v2)
    return edge_path_dict

# Called in create_edge_path_dict
def join_paths(path_dict, v1, v2):
    v1 = int(v1)
    v2 = int(v2)
    v1_v2 = path_dict[v1][v2]
    v2_v1 = path_dict[v2][v1]
    if min(len(v1_v2), len(v2_v1)) == 0:
        if len(v1_v2) == 0:
            return v2_v1
        elif len(v2_v1) == 0:
            return v1_v2
    else:
        i = 0
        while i < min(len(v1_v2), len(v2_v1)):
            if v1_v2[i] == v2_v1[i]:
                i += 1
            else:
                break
        reversed_v1_v2 = list(reversed(v1_v2))
        joined_path = reversed_v1_v2[:-i] + v2_v1[i - 1:]
        return joined_path

# Called in get_unique_paths
def create_empty_path_dict(G_st, non_st_edges_list):
    path_dict = {}
    for edge in non_st_edges_list:
        path_dict[edge[0]] = {}
        path_dict[edge[1]] = {}
    for edge in non_st_edges_list:
        path_dict[edge[0]][edge[1]] = []
        path_dict[edge[1]][edge[0]] = []
    return path_dict

# Called in balance_graph
def get_unique_paths(G_st, non_st_edges_list):
    path_dict = create_empty_path_dict(G_st, non_st_edges_list)
    search_children(G_st, None, 0, path_dict, [])
    edge_path_dict = create_edge_path_dict(path_dict)
    del path_dict
    return edge_path_dict   

# Called in process_locally
def balance_graph(b_unbalanced_csr_adj_matrix, tree_name, config_obj, mapping_to_original, rand_weights, node_index):
    start_balance = datetime.now()
    print("Begin graph balancing: ", str(datetime.now()))
    changed_edge_list = []
    tree_type = get_tree_type(config_obj)
    print("Tree type: --------------------> " ,tree_type)
    csr_st_adj_matrix = get_spanning_tree(b_unbalanced_csr_adj_matrix, tree_type ,tree_name, rand_weights, node_index) # types: random, random_MST, breadth, depth
    print('Random Tree Acquired, took: (hh:mm:ss.ms) {}'.format(datetime.now() - start_balance))
    non_st_edges_list = get_non_st_edges(b_unbalanced_csr_adj_matrix, csr_st_adj_matrix)
    nx_st_graph = nx.from_scipy_sparse_matrix(csr_st_adj_matrix)
    begin_get_edges_to_change = datetime.now()
    unique_paths = get_unique_paths(nx_st_graph, non_st_edges_list)
    changed_edge_list = [edge_to_change for edge_to_change in (should_change_edge(nx_st_graph, unique_paths, coord_triple) for coord_triple in non_st_edges_list) if edge_to_change is not None]

    print('Got changed edges, took: (hh:mm:ss.ms) {}'.format(datetime.now() - begin_get_edges_to_change))
    csr_bal_adj_matrix = reverse_edges(b_unbalanced_csr_adj_matrix, changed_edge_list)
    print('Balancing time elapsed: (hh:mm:ss.ms) {}'.format(datetime.now() - start_balance))
   
    write_balanced_h5(config_obj, mapping_to_original, b_unbalanced_csr_adj_matrix, csr_st_adj_matrix, nx_st_graph, csr_bal_adj_matrix, changed_edge_list, tree_name)
    del csr_st_adj_matrix
    del csr_bal_adj_matrix
    del changed_edge_list
    gc.collect()
    return tree_name

# Called in balance_graph
def get_non_st_edges(csr_unbal_adj_matrix, csr_st_adj_matrix):
    non_st_edges_list = None
    if hasattr(csr_unbal_adj_matrix, 'value'):
        rows, cols = (csr_unbal_adj_matrix.value - csr_st_adj_matrix).nonzero()
        non_st_edges_list = [(rows[i], cols[i], csr_unbal_adj_matrix.value[rows[i], cols[i]]) for i in range(len(rows)) if cols[i] > rows[i]]
    else:
        rows, cols = (csr_unbal_adj_matrix - csr_st_adj_matrix).nonzero()
        non_st_edges_list = [(rows[i], cols[i], csr_unbal_adj_matrix[rows[i], cols[i]]) for i in range(len(rows)) if cols[i] > rows[i]]
    return non_st_edges_list

# Called in balance_graph
def should_change_edge(st_graph, unique_paths, coord_triple):
    cycle_list = unique_paths[(coord_triple[0], coord_triple[1])]
#    print("cycle list: ", cycle_list)
#    print("coord triple: ", coord_triple)
#    print("cycle list iterated through")
#    for i, j in zip(cycle_list, cycle_list[1:]):
#        print(i,j)
    cycle_sign_list = [ st_graph[i][j]['weight'] for i, j in zip(cycle_list, cycle_list[1:]) ] 
#    print("cycle sign list before append:", cycle_sign_list)
    cycle_sign_list.append(coord_triple[2])
#    print("cycle sign list after append:", cycle_sign_list)
    if prod(cycle_sign_list) == -1:
        return coord_triple
    else:
        return None

# Called in reverse_edge
def reverse_edge(csr_adj_matrix, coord_triple):
    csr_adj_matrix[coord_triple[0], coord_triple[1]] = 0 - csr_adj_matrix[coord_triple[0], coord_triple[1]]
    csr_adj_matrix[coord_triple[1], coord_triple[0]] = 0 - csr_adj_matrix[coord_triple[1], coord_triple[0]]
    return True # reversed successfully

# Called in balance_graph
def reverse_edges(csr_unbal_adj_matrix, list_of_edges_to_change):
    csr_bal_adj_matrix = None
    if hasattr(csr_unbal_adj_matrix, 'value'):
        csr_bal_adj_matrix = csr_unbal_adj_matrix.value.copy()
    else:
        csr_bal_adj_matrix = csr_unbal_adj_matrix.copy()
    print("Number of edges to change: ", len(list_of_edges_to_change))
    for coord_triple in list_of_edges_to_change:
        reverse_edge(csr_bal_adj_matrix, coord_triple)
    return csr_bal_adj_matrix

def get_tree_type(config_obj):
    tree_options = config_obj["tree_type"]
    if tree_options["random_MST"]:
        tree_type = "random_MST"
    elif tree_options["breadth"]:
        tree_type = "breadth"
    elif tree_options["depth"]:
        tree_type = "depth"
    return tree_type




##########################################################################################
			 ########## Balanced H5 Writing ##########
##########################################################################################

# Called in write_balanced_h5
def create_matrix_h5_file(g, csr_m):
    g.create_dataset('data', data = csr_m.data)
    g.create_dataset('indptr', data = csr_m.indptr)
    g.create_dataset('indices', data = csr_m.indices)
    g.attrs['shape'] = csr_m.shape


### This function will write csr matrices to csv, it drops all the zeros when writing.
def write_csr_to_csv(csr_matrix, name):
    graph = csr_matrix.toarray()
    filename = name
    print("length of graph array:", len(graph))
    print("csr matrix array:", graph)
    print("length of one row:", len(graph[0]))
    with open(filename , 'w') as writefile:
        writer = csv.writer(writefile)
        writer.writerow(['From', 'To', 'Weight'])
        print("WRITING CSR MATRIX TO CSV AT: ", filename )
        for (m, n), value in np.ndenumerate(graph):
            if value != 0:
                writer.writerow([m, n, value])

# Called in write_balanced_h5
### As of 5/31/20 this function will run very slow in datasets with high number of nodes. 
### Needs a fix that doesn't rely on so many dictionary lookups to add the size to the comopnent list
def write_component_stats(f, csr_bal_adj_matrix, csr_st_adj_matrix, component_list):
    f.create_dataset('component_list', data = component_list)
    total_nodes = csr_st_adj_matrix.shape[0]
    unique, counts = np.unique(component_list, return_counts=True)
    f.attrs['c' + str(unique[0]) + '_vertex_size'] = int(counts[0])
    if (len(unique) > 1):
        f.attrs['c' + str(unique[1]) + '_vertex_size'] = int(counts[1])
        f.attrs['total_vertex_size'] = int(counts[0]) + int(counts[1])
        assert(int(counts[0]) + int(counts[1]) == csr_bal_adj_matrix.shape[0])
        assert(int(counts[0]) + int(counts[1]) == csr_st_adj_matrix.shape[0])
### Comment out lines 327 - 332 if you don't want to compute and create the weighted component list        
        c0_size_percent = f.attrs['c0_vertex_size'] / total_nodes
        c1_size_percent = f.attrs['c1_vertex_size'] / total_nodes
        component_list_dict = dict(enumerate(component_list))

        component_list_with_tuples = [(component_list_dict[entry], c0_size_percent) if component_list_dict[entry] == 0 else (component_list_dict[entry], c1_size_percent) for entry in range(total_nodes)]
        f.create_dataset('weighted_component_list', data = component_list_with_tuples)
    else:
        print("component list only contains one component")
        f.attrs['total_vertex_size'] = int(counts[0])
        assert(int(counts[0] == csr_bal_adj_matrix.shape[0]))
        assert(int(counts[0] == csr_st_adj_matrix.shape[0]))

def get_components_avg_degree(balanced_graph_degree_list, component_list):
    degree_c0_total = 0
    degree_c1_total = 0
    c0_count = 0
    c1_count = 0
    
    for index in range(len(balanced_graph_degree_list)):
        if component_list[index] == 0:
            degree_c0_total += balanced_graph_degree_list[index]
            c0_count += 1
        elif component_list[index] == 1:
            degree_c1_total += balanced_graph_degree_list[index]
            c1_count += 1
    assert(c0_count + c1_count == len(component_list))
#    print("balanced degree list: ", balanced_graph_degree_list)
#    print("degree total c0:", degree_c0_total)
#    print("degree total c1:", degree_c1_total)

    avg_deg_c0 = degree_c0_total/c0_count
    avg_deg_c1 = degree_c1_total/c1_count
    
    return avg_deg_c0, avg_deg_c1

# Called in write_balanced_h5
def write_vertex_degree_stats(f, csr_bal_adj_matrix, csr_st_adj_matrix, component_list):
    vertex_neighbor_amt_list = csr_st_adj_matrix.getnnz(axis=1)
    balanced_graph_degree_list = csr_bal_adj_matrix.getnnz(axis=1)
    #print("vertex neighbor amt list", vertex_neighbor_amt_list)
    avg_deg_c0, avg_deg_c1 = get_components_avg_degree(balanced_graph_degree_list, component_list)
    f.attrs['mean_tree_vertex_deg'] = np.mean(vertex_neighbor_amt_list)
    f.attrs['stdev_tree_vertex_deg'] = np.sqrt(np.var(vertex_neighbor_amt_list))
  #  f.attrs['avg_deg_c0'] = avg_deg_c0
  #  f.attrs['avg_deg_c1'] = avg_deg_c1
    num_p, num_p_0, num_p_1 = get_num_pendant_vertices(vertex_neighbor_amt_list, component_list)
    f.attrs['pendant_vertices_c0'] = num_p_0
    f.attrs['pendant_vertices_c1'] = num_p_1
    f.attrs['pendant_vertices_total'] = num_p

    f.create_dataset('vertex_neighbor_amt_list', data = vertex_neighbor_amt_list)

	
# Called in balance_graph
def write_balanced_h5(config_obj, mapping_to_original, b_csr_unbal_adj_matrix, csr_st_adj_matrix,
                        nx_st_graph, csr_bal_adj_matrix, changed_edge_list, tree_name):
    bal_adj_path = get_balanced_h5_path(config_obj) + tree_name + ".h5"
    print("Writing balanced h5: ", "(", tree_name, ", ", config_obj['dataset'], ", ", config_obj['data_subset_type'], ", ", config_obj['matrix_name'], ", ", config_obj['component_no'], ") ")
    try:
        start_component_list = datetime.now()
        component_list = get_balance_components(nx_st_graph)
        print('Component List Acquired, took: (hh:mm:ss.ms) {}'.format(datetime.now() - start_component_list))
        num_components = np.unique(component_list)
        if len(num_components) > 1:
            f = h5py.File(bal_adj_path, 'w')
            g = f.create_group("csr_st_adj_matrix")
            create_matrix_h5_file(g, csr_st_adj_matrix)
            h = f.create_group("csr_bal_adj_matrix")
            create_matrix_h5_file(h, csr_bal_adj_matrix)
            f.create_dataset('changed_edge_list', data = changed_edge_list)
            f.create_dataset('mapping_to_original', data = mapping_to_original)
            write_component_stats(f, csr_bal_adj_matrix, csr_st_adj_matrix, component_list)
            write_vertex_degree_stats(f, csr_bal_adj_matrix, csr_st_adj_matrix, component_list) 
            write_edge_stats(f, b_csr_unbal_adj_matrix, csr_bal_adj_matrix)
            write_balanced_attributes(f, config_obj, tree_name)
            if config_obj['has_labels']: ## wrties c0 and c1 wins and losses to existing h5
                write_outcome_stats(f, config_obj, csr_bal_adj_matrix, component_list)
            print("Wrote balanced h5: ", "(", tree_name, ", ", config_obj['dataset'], ", ", config_obj['data_subset_type'], ", ", config_obj['matrix_name'], ", ", config_obj['component_no'], ")")
            f.close()
        else:
            print("Component list had only one component. No Agreeable Minority exists for this tree. Tree not saved to h5.")     
    finally:
        print()
#        f.close()
#    print("Wrote balanced h5: ", "(", tree_name, ", ", config_obj['dataset'], ", ", config_obj['data_subset_type'], ", ", config_obj['matrix_name'], ", ", config_obj['component_no'], ")")

def get_neighbors(vertex_number, graph_adj_matrix):
    neighbors = []
    if isinstance(graph_adj_matrix, np.ndarray):
        neighbors = [index for index, adjacency in enumerate(graph_adj_matrix[vertex_number]) if adjacency != 0]
    else:
        neighbors = list(np.split(graph_adj_matrix.indices, graph_adj_matrix.indptr)[vertex_number + 1:vertex_number + 2][0]) # gets a list of neighbors of vertex <vertex_number>
    return neighbors

def flip(element):
    if element == 1:
        return 0
    elif element == 0:
        return 1
    else:
        return -1

# Called by get_balance_components
def get_unvisited_neighbors(visited, nx_st_graph):
    neighbor_lists = [nx_st_graph.neighbors(visited_vertex) for visited_vertex in visited]
    all_neighbors = set([vertex for neighbor_list in neighbor_lists for vertex in neighbor_list])
    unvisited_neighbors = all_neighbors - visited
    return unvisited_neighbors

def assign_component_numbers(component_list, unvisited_neighbors, visited, nx_st_graph):
    for vertex in unvisited_neighbors:
        neighbors = nx_st_graph.neighbors(vertex)
        visited_neighbors = list(set(neighbors) & visited)
        neighbor = visited_neighbors[0]
        edge = nx_st_graph.get_edge_data(neighbor, vertex)
        if edge['weight'] < 0:
            if component_list[neighbor] == 0:
                component_list[vertex] = 1
            elif component_list[neighbor] == 1:
                component_list[vertex] = 0
        elif edge['weight'] > 0:
            component_list[vertex] = component_list[neighbor]
    return component_list

def get_balance_components(nx_st_graph):
    NUM_VERTICES = len(nx_st_graph)
    component_list = [-1 for i in range(NUM_VERTICES)]
    visited = set([0])
    component_list[0] = 0
    while len(visited) < NUM_VERTICES:
        unvisited_neighbors = get_unvisited_neighbors(visited, nx_st_graph)
        component_list = assign_component_numbers(component_list, unvisited_neighbors, visited, nx_st_graph)
        visited = visited | unvisited_neighbors
    c0_amt = component_list.count(0)
    c1_amt = component_list.count(1)
    if c0_amt < c1_amt:
        component_list = [flip(element) for element in component_list]
    assert(-1 not in component_list)
    assert(None not in component_list)
    return component_list

def write_edge_stats(f, b_csr_unbal_adj_matrix, csr_bal_adj_matrix):
    total_edges = csr_bal_adj_matrix.count_nonzero() / 2
    total_vertices = csr_bal_adj_matrix.shape[0]
    rows, cols = csr_bal_adj_matrix.nonzero()

    if hasattr(b_csr_unbal_adj_matrix, 'value'):
        b_csr_unbal_adj_matrix = b_csr_unbal_adj_matrix.value
    total_neg = len([i for i in range(len(rows)) if b_csr_unbal_adj_matrix[rows[i], cols[i]] == -1]) / 2
    total_pos = len([i for i in range(len(rows)) if b_csr_unbal_adj_matrix[rows[i], cols[i]] ==  1]) / 2
    assert(total_edges == total_neg + total_pos)
    pos_to_neg = len([i for i in range(len(rows)) if b_csr_unbal_adj_matrix[rows[i], cols[i]] ==  1 and csr_bal_adj_matrix[rows[i], cols[i]] == -1]) / 2
    neg_to_pos = len([i for i in range(len(rows)) if b_csr_unbal_adj_matrix[rows[i], cols[i]] == -1 and csr_bal_adj_matrix[rows[i], cols[i]] ==  1]) / 2
    pos_to_pos = len([i for i in range(len(rows)) if b_csr_unbal_adj_matrix[rows[i], cols[i]] ==  1 and csr_bal_adj_matrix[rows[i], cols[i]] ==  1]) / 2
    neg_to_neg = len([i for i in range(len(rows)) if b_csr_unbal_adj_matrix[rows[i], cols[i]] == -1 and csr_bal_adj_matrix[rows[i], cols[i]] == -1]) / 2
    assert(pos_to_pos + pos_to_neg == total_pos)
    assert(neg_to_pos + neg_to_neg == total_neg)
    assert(pos_to_neg >= 0)
    assert(neg_to_pos >= 0)
    assert(pos_to_pos >= 0)
    assert(neg_to_neg >= 0)

    f.attrs['total_edges'] = total_edges
    f.attrs['total_neg_edges'] = total_neg
    f.attrs['total_pos_edges'] = total_pos

    f.attrs['++_edges'] = pos_to_pos
    f.attrs['--_edges'] = neg_to_neg
    f.attrs['+-_edges'] = pos_to_neg
    f.attrs['-+_edges'] = neg_to_pos
    f.attrs['num_changed_edges'] = pos_to_neg + neg_to_pos
    f.attrs['cyclomatic_num'] = total_edges - total_vertices + 1

def write_balanced_attributes(f, config_obj, tree_name):
    f.attrs['component_no'] = config_obj['component_no']
    f.attrs['data_subset_type'] = config_obj['data_subset_type']
    f.attrs['dataset'] = config_obj['dataset']
    f.attrs['matrix_name'] = config_obj['matrix_name']
    f.attrs['from_clustering'] = False
    f.attrs['is_symmetric'] = True
    
def identify_record(outcome):
    if outcome == 1:
        return 'W'
    elif outcome == 0:
        return 'L'
    else:
        return 'N'

def write_outcome_stats(f, config_obj, csr_bal_adj_matrix, component_map_list):

    matrix_file_path = get_full_sym_h5_path(config_obj)
    outcomes = None
    try:
        full_h5 = h5py.File(matrix_file_path + str(config_obj['component_no']) + ".h5", 'r')
        outcomes = list(full_h5['outcomes'])
        
    finally:
        full_h5.close()
    f.create_dataset("outcomes", data=outcomes)

    vertex_outcome_component_dict = {
        vertex: {"C": component_map_list[vertex], "O": identify_record(outcomes[vertex])} for vertex in range(csr_bal_adj_matrix.shape[0])
    } ## assigns component and outcome for each vertex assigned sequentially not by node ID
    vertex_outcome_component_df = pd.DataFrame(vertex_outcome_component_dict).T

    c0 = vertex_outcome_component_df.loc[vertex_outcome_component_df['C'] == 0]
    c1 = vertex_outcome_component_df.loc[vertex_outcome_component_df['C'] == 1]

    c0_W = c0.loc[c0['O'] == 'W']
    c0_L = c0.loc[c0['O'] == 'L']
    c0_N = c0.loc[c0['O'] == 'N']
    c1_W = c1.loc[c1['O'] == 'W']
    c1_L = c1.loc[c1['O'] == 'L']
    c1_N = c1.loc[c1['O'] == 'N']

    f.attrs['c0_wins'] = len(c0_W)
    f.attrs['c0_losses'] = len(c0_L)
    f.attrs['c0_nones'] = len(c0_N)
    f.attrs['c1_wins'] = len(c1_W)
    f.attrs['c1_losses'] = len(c1_L)
    f.attrs['c1_nones'] = len(c1_N)

    T0 = c0_W + c0_L
    T1 = c1_W + c1_L
    bias = -999
    try:
        bias = float(len(c0_W) / len(T0)) - float(len(c1_W) / len(T1))
    except ZeroDivisionError:
        print("Warning: Either c0 or c1 is missing at least one winner or at least one loser. Bias score set to: -999")
    f.attrs['tree_bias_score'] = bias

# Called in 
def get_num_pendant_vertices(neighbors_len_list, component_list):
    num_p = 0
    num_p_0 = 0
    num_p_1 = 0
    for i, vertex in enumerate(neighbors_len_list):
        if int(vertex) == 1:
            num_p += 1
            if component_list[i] == 0:
                num_p_0 += 1
            elif component_list[i]== 1:
                num_p_1 += 1
    return num_p, num_p_0, num_p_1

# Called in process_locally
def generate_tree_names(config_obj):
    tree_names = [str(uuid.uuid4()) for i in range(config_obj['num_random_trees'])]
    return tree_names

# Called in process_locally
def get_mapping_to_original(config_obj, local_override=False):
    matrix_file_path = get_full_sym_h5_path(config_obj, local_override)
    mapping_to_original = None
    try:
        f = h5py.File(matrix_file_path + str(config_obj['component_no']) + ".h5", 'r')
        mapping_to_original = list(f['mapping_to_original'])
    finally:
        f.close()
    return mapping_to_original

# Called in process_locally
def broadcast_dump(self, value, f):
    print("Dumping file. value / file size: ", sys.getsizeof(value), " / ", sys.getsizeof(f))
    pickle.dump(value, f, 4)  # was 2, 4 is first protocol supporting >4GB
    f.close()
    print("~~~~~~~~~~~ DUMPED! ~~~~~~~~~~~~")
    return f.name

def process_locally(config_obj):
    tree_names_to_create = generate_tree_names(config_obj)
    #tree_names_to_create_tuples = list()
    #for item in range(len(tree_names_to_create)):
    #    tree_names_tuple = (0, item)
    #    tree_names_to_create_tuples.append(tree_names_tuple)
    #for item in range(len(tree_names_to_create_tuples)):
    #    tree_names_to_create_tuples[item] = (tree_names_to_create[item], tree_names_to_create_tuples[item][1])
         
    
    print("Creating ", len(tree_names_to_create), " trees.")
    balanced_tuple_list = None
    unbalanced_csr_adj_matrix = get_full_csr_adj(config_obj, True)
    
    #### This block used to write the interim csr matrix to csv if needed ####
    #graph = unbalanced_csr_adj_matrix.toarray()
    #print("after graph declare")
    #with open('lastvotetest.csv', 'w') as writefile:
    #    writer = csv.writer(writefile)
    #    writer.writerow(['from', 'to', 'weight'])
    #    print("in file statement")
    #    for (m, n), value in np.ndenumerate(graph):
    #        if value != 0:
    #            print("writing to file")
    #            writer.writerow([m, n, value])
    mapping_to_original = get_mapping_to_original(config_obj, True) 
    num_edges_in_graph = int(unbalanced_csr_adj_matrix.count_nonzero() / 2)
    random_weights_dict = {}
    for tree_name in tree_names_to_create:
        random_weights_dict[tree_name] = np.random.uniform(0, 1, num_edges_in_graph)
    if config_obj['parallelism'] == 'spark': # Use Spark
        print("Paralellism: Spark")
        from pyspark import SparkContext, SparkConf, broadcast
        # https://datascience.stackexchange.com/questions/8549/how-do-i-set-get-heap-size-for-spark-via-python-notebook
        # https://stackoverflow.com/questions/50865093/modulenotfounderror-in-pyspark-worker-on-rdd-collect
        conf = SparkConf().setAppName("Balancer")
        conf = (conf.setMaster('local[*]') # conf = (conf.setMaster('local[*]')
        .set('spark.executor.memory', '100G')
        .set('spark.driver.memory', '100G')
        .set('spark.driver.maxResultSize', '16G')
        .set('spark.cleaner.ttl', 86400 * 2)
        .set("spark.local.dir", "~/tmp/spark-temp"))
        sc = SparkContext(conf=conf)

        broadcast.Broadcast.dump = broadcast_dump
        print("unbalanced_csr_adj_matrix edges / vertices: ", num_edges_in_graph, " / ", unbalanced_csr_adj_matrix.shape[0])
        print("Size of unbalanced_csr_adj_matrix in bytes: ", sys.getsizeof(unbalanced_csr_adj_matrix))
        print("Size of unbalanced_csr_adj_matrix in gigabytes: ", sys.getsizeof(unbalanced_csr_adj_matrix) / (1024 * 1024 * 1024))
        # b_unbalanced_csr_adj_matrix = sc.broadcast(unbalanced_csr_adj_matrix)
        tree_names_to_create_rdd = sc.parallelize(tree_names_to_create)
        # balanced_tuple_list = tree_names_to_create_rdd.map(lambda tree_name: balance_graph(b_unbalanced_csr_adj_matrix, tree_name, config_obj, mapping_to_original, random_weights_dict))
        balanced_tuple_list = tree_names_to_create_rdd.map(lambda tree_name: balance_graph(unbalanced_csr_adj_matrix, tree_name, config_obj, mapping_to_original, random_weights_dict))
        balanced_tuple_list = balanced_tuple_list.collect()
        # b_unbalanced_csr_adj_matrix.unpersist()
    elif config_obj['parallelism'] == 'parallel': # Do regular parallel
        print("Paralellism: Regular Parallel")
        balanced_tuple_list = Parallel(n_jobs=-1, prefer="threads")(delayed(balance_graph)(unbalanced_csr_adj_matrix, tree_name, config_obj, mapping_to_original, random_weights_dict) for tree_name in tree_names_to_create)
    elif config_obj['parallelism'] == 'serial':
        print("Paralellism: Serial")
        balanced_tuple_list = list()
        node_index = 0 
        for tree_name in tree_names_to_create: 
            if node_index == len(mapping_to_original):
                node_index = 0
                print("NODE INDEX RESET, THERE ARE LESS NODES THAN NUMBER OF BREADTH TREES REQUESTED")
            balanced_tuple_list.append(balance_graph(unbalanced_csr_adj_matrix, tree_name, config_obj, mapping_to_original, random_weights_dict, node_index))
            node_index += 1
    print("----------")
    if len(balanced_tuple_list) > 0:
        print("Trees made: ", len(balanced_tuple_list))
    else:
        print("No trees made.")
    print("----------")
    return 0

def submit_process_LEAP_job(config_obj, preprocess_jobID):
  # retrieve (dataset, data_subset_type, matrix_name, component_no) from config_obj
  dataset = config_obj['dataset']
  data_subset_type = config_obj['data_subset_type']
  matrix_name = config_obj['matrix_name']
  component_no = config_obj['component_no']
  # then call a bash script that calls preprocess_general with those parameters
  # subprocess.check_call("preprocess_general.sh %s %s %s %s" % (dataset, data_subset_type, matrix_name, str(component_no)))
  LEAP_output = None
  if config_obj['parallelism'] == 'spark':
    print("Submitting process job on LEAP using Spark")
    LEAP_output = subprocess.run(['process/wrapper_process_general_spark.sh', dataset, data_subset_type, matrix_name, str(component_no), str(preprocess_jobID)], stdout=subprocess.PIPE).stdout.decode('utf-8')
  else:
    print("Submitting process job on LEAP (non-Spark).")
    LEAP_output = subprocess.run(['process/wrapper_process_general.sh', dataset, data_subset_type, matrix_name, str(component_no), str(preprocess_jobID)], stdout=subprocess.PIPE).stdout.decode('utf-8')
  print("submit_process_LEAP_job output: ", LEAP_output)
  job_ID = int(LEAP_output.split()[-1])
  return job_ID

if __name__ == "__main__":
  print("Running process main with args: ", sys.argv)
  dataset = str(sys.argv[1])
  data_subset_type = str(sys.argv[2])
  matrix_name = str(sys.argv[3])
  component_no = int(sys.argv[4])
  preprocess_jobID = int(sys.argv[5])
  config_obj = get_yaml_config_obj_by_key_tuple(dataset, data_subset_type, matrix_name, component_no)
  process_locally(config_obj)
