import sys
sys.path.append("..")

import pandas as pd
import numpy as np
import h5py
import os
import time
import pickle
import multiprocessing as mp
from os import listdir
from os.path import isfile, join, splitext, dirname, abspath
from joblib import Parallel, delayed

from dataset_paths import get_balanced_h5_path, get_df_folder, get_full_csr_adj, get_balanced_csr_adj, get_tree_csr_adj, get_raw_dataset_csv_path

def get_balanced_file_list(config_obj, local_override=False):
    BALANCED_DIR = get_balanced_h5_path(config_obj, local_override)
    balanced_file_list = [f for f in listdir(BALANCED_DIR) if isfile(join(BALANCED_DIR, f)) if f != '.DS_Store']
    balanced_file_list.sort()
    print("Tree list Length: ", len(balanced_file_list))
    return balanced_file_list

def postprocess_all_dfs(config_obj):
    postprocess_tree_df(config_obj)
    postprocess_vertex_df(config_obj)

########################################################################
### Calculate tree dfs
########################################################################

def get_tree_df_tup(tree, config_obj):
    return (tree, get_tree_df_row(tree, config_obj))

def get_tree_df_row(tree, config_obj):
    balanced_h5_file = get_balanced_h5_path(config_obj, True) + tree
    balanced_h5 = None
    row = {}
    try:
        balanced_h5 = h5py.File(balanced_h5_file, 'r')
        row = {
            "pv_c0_pct": 100 * (balanced_h5.attrs['pendant_vertices_c0'] / (balanced_h5.attrs['pendant_vertices_c0'] + balanced_h5.attrs['pendant_vertices_c1'])),
            "pv_c1_pct":  100 * (balanced_h5.attrs['pendant_vertices_c1'] / (balanced_h5.attrs['pendant_vertices_c0'] + balanced_h5.attrs['pendant_vertices_c1'])),
            "pv_pct": 100 * ((balanced_h5.attrs['pendant_vertices_c0'] + balanced_h5.attrs['pendant_vertices_c1']) / balanced_h5.attrs['total_vertex_size']),
            "tree_pendant_vertices": balanced_h5.attrs['pendant_vertices_c0'] + balanced_h5.attrs['pendant_vertices_c1'],
            "c0_pct": (balanced_h5.attrs['c0_vertex_size'] / (balanced_h5.attrs['c0_vertex_size'] + balanced_h5.attrs['c1_vertex_size'])) * 100,    
            "++_edges": balanced_h5.attrs['++_edges'],
            "-+_edges": balanced_h5.attrs['-+_edges'],
            "+-_edges": balanced_h5.attrs['+-_edges'],
            "--_edges": balanced_h5.attrs['--_edges'],
            "num_changed_edges": balanced_h5.attrs['num_changed_edges'],
            "mean_tree_vertex_deg": balanced_h5.attrs['mean_tree_vertex_deg'],
            "stdev_tree_vertex_deg": balanced_h5.attrs['stdev_tree_vertex_deg']
        }
        if 'tree_bias_score' in balanced_h5.attrs:
            row["tree_bias_score"] = balanced_h5.attrs['tree_bias_score']
        balanced_h5.close()
    except Exception as error:
        print("Tree DF OSError. The following tree is bad: ", tree, " - path: ", balanced_h5_file)
        print(error)
   #     os.remove(balanced_h5_file)
    return row

def postprocess_tree_df(config_obj, dont_remake_override=False):
    DF_FOLDER = get_df_folder(config_obj)
    FULL_DF_PATH = DF_FOLDER + config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_" + str(config_obj['component_no']) + "_tree_df.pkl"
    tree_df = None
    print("-------- Entering Post-Process Tree DF --------")
    if (not isfile(FULL_DF_PATH) or config_obj['postprocess_again']) and not dont_remake_override:
        print("-------- Creating Tree DF --------")
        # if (it's not a file or we want to remake it) AND we're not calling this function from a plotting fn, table fn, etc...
        to_be_df_dict = None
        trees_list = get_balanced_file_list(config_obj, True)
        if config_obj['parallelism'] == 'parallel' or config_obj['parallelism'] == 'spark':
            num_cores = mp.cpu_count()
            print("Creating tree df (parallel: ", num_cores, " cores):", config_obj['dataset'], ", ", config_obj['data_subset_type'], ", ", config_obj['matrix_name'], ", ", config_obj['component_no'], ") ")
            df_tup_list = Parallel(n_jobs=num_cores)(delayed(get_tree_df_tup)(tree, config_obj) for tree in trees_list)
            to_be_df_dict = {tup[0]: tup[1] for tup in df_tup_list}
        elif config_obj['parallelism'] == 'serial':
            print("Creating tree df (serial):", config_obj['dataset'], ", ", config_obj['data_subset_type'], ", ", config_obj['matrix_name'], ", ", config_obj['component_no'], ") ")
            to_be_df_dict = {
                tree: get_tree_df_row(tree, config_obj) for tree in trees_list
            }
            tree_df = pd.DataFrame(to_be_df_dict).T
        pd.to_pickle(tree_df, FULL_DF_PATH)
        print("Done. Made tree df of shape: ", tree_df.shape)
    else:
        print("-------- Reading Tree DF --------")
        tree_df = pd.read_pickle(FULL_DF_PATH)
    return tree_df

########################################################################
### Calculate vertex dfs
########################################################################

def postprocess_vertex_df(config_obj, dont_remake_override=False):
    DF_FOLDER = get_df_folder(config_obj)
    FULL_DF_PATH = DF_FOLDER + config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_" + str(config_obj['component_no']) + "_vertex_df.pkl"
    vertex_df = None
    print("-------- Entering Post-Process Vertex DF --------")
    if (not isfile(FULL_DF_PATH) or config_obj['postprocess_again']) and not dont_remake_override:
        print("-------- Creating Vertex DF --------")
        # if (it's not a file or we want to remake it) AND we're not calling this function from a plotting fn, table fn, etc...
        to_be_df_dict = None
        trees_list = get_balanced_file_list(config_obj, True)
        if config_obj['parallelism'] == 'parallel' or config_obj['parallelism'] == 'spark':
            num_cores = mp.cpu_count()
            print("Creating vertex df (parallel: ", num_cores, " cores):", config_obj['dataset'], ", ", config_obj['data_subset_type'], ", ", config_obj['matrix_name'], ", ", config_obj['component_no'], ") ")
            df_tup_list = Parallel(n_jobs=num_cores)(delayed(get_per_tree_vertex_dict_tup)(tree, config_obj) for tree in trees_list)
            to_be_df_dict = {tup[0]: tup[1] for tup in df_tup_list}
            print("Finished base, adding component and outcome columns.")
        elif config_obj['parallelism'] == 'serial':
            print("Creating vertex df (serial):", config_obj['dataset'], ", ", config_obj['data_subset_type'], ", ", config_obj['matrix_name'], ", ", config_obj['component_no'], ") ")
            to_be_df_dict = {
                tree: get_per_tree_vertex_dict(tree, config_obj) for tree in trees_list
            }
            print("Finished base, adding component and outcome columns.")
        vertex_df = create_vertex_df_from_vertex_dict(to_be_df_dict, config_obj, trees_list, FULL_DF_PATH)
    else:
        print("-------- Reading Vertex DF --------")
        vertex_df = pd.read_pickle(FULL_DF_PATH)
    return vertex_df

def get_users_map(config_obj):
    map_csv_path = get_raw_dataset_csv_path(config_obj) + "_map.csv"

    if os.path.isfile(map_csv_path):
        users_map_df = pd.read_csv(map_csv_path)
        ignore = False
    else:
        print("No file in map_csv path!!")
        users_map_df = None
        ignore = True        
    return users_map_df, ignore

def create_vertex_df_from_vertex_dict(to_be_df_dict, config_obj, trees_list, FULL_DF_PATH):
    print("Creating components dict.")
    try:
        components_dict = {tree: to_be_df_dict[tree]['component_list'] for tree in trees_list}
        component_df = pd.DataFrame(components_dict)
        component_dict_with_weights = {tree: to_be_df_dict[tree]['component_list_with_tuples'] for tree in trees_list}
        component_weights_df = pd.DataFrame(component_dict_with_weights)
    except:
        print("tree without component list found, moving to next.")
        
    balanced_h5_file = get_balanced_h5_path(config_obj, True) + trees_list[0]
    try:
        balanced_h5 = h5py.File(balanced_h5_file, 'r')
        print("Adding c0 pct (and outcomes if applicable).")
        vertex_df = add_c0_pct_and_outcomes(trees_list[0], balanced_h5, component_weights_df, config_obj['tiebreak_node'], config_obj['weighted_status'])
        pd.to_pickle(vertex_df, FULL_DF_PATH)
        print("Done. Made vertex df of shape: ", vertex_df.shape)
    finally:
        balanced_h5.close()
    return vertex_df

def get_per_tree_vertex_dict_tup(tree, config_obj):
    return (tree, get_per_tree_vertex_dict(tree, config_obj))

def get_per_tree_vertex_dict(tree, config_obj): 
    balanced_h5_file = get_balanced_h5_path(config_obj, True) + tree
    balanced_h5 = None
    row = {}
    try:
        balanced_h5 = h5py.File(balanced_h5_file, 'r')
### TODO: Make this a config option in the yaml file instead of comment/uncomment
### This block can be uncommented to add the c0 and c1 size percentages to Data h5s that have already been made. 
        total_nodes = balanced_h5.attrs['c0_vertex_size'] + balanced_h5.attrs['c1_vertex_size']
        c0_size_percent = balanced_h5.attrs['c0_vertex_size'] / total_nodes
        c1_size_percent = balanced_h5.attrs['c1_vertex_size'] / total_nodes
        component_list_dict = dict(enumerate(balanced_h5['component_list']))
        
        component_list_with_tuples = [(component_list_dict[entry], c0_size_percent) if component_list_dict[entry] == 0 else (component_list_dict[entry], c1_size_percent) for entry in range(total_nodes)]

### These next two lines should be switched depending on if the c0 and c1 size were added when the trees were initially run or not. If they were not, use line 176 and the block above. If they were, use line 177.
        row['component_list_with_tuples'] = component_list_with_tuples
#        row['component_list_with_tuples'] = list(balanced_h5['weighted_component_list'])
        row['component_list'] = list(balanced_h5['component_list']) 
        row['vertex_neighbor_amt_list'] = list(balanced_h5['vertex_neighbor_amt_list'])
        row['mean_tree_vertex_deg'] = balanced_h5.attrs['mean_tree_vertex_deg']
        row['stdev_tree_vertex_deg'] = balanced_h5.attrs['stdev_tree_vertex_deg']
        row['pendant_vertices_c0'] = balanced_h5.attrs['pendant_vertices_c0']
        row['pendant_vertices_c1'] = balanced_h5.attrs['pendant_vertices_c1']
        row['pendant_vertices_total'] = balanced_h5.attrs['pendant_vertices_total']
        balanced_h5.close()
    except Exception as error:
        print("Vertex DF error. The following tree is bad. ", tree, " - path: ", balanced_h5_file)
        print("error: " , error)
        ## Eric commented out this line so things can be tested in this function without deleting tree files.
 #       os.remove(balanced_h5_file)
    return row

def calc_weighted_status(component_df, df_transpose, tiebreak_node, weighted_status_flag):
    status_list = []
    if not weighted_status_flag:
        print("running without weighted status, tiebreak node is:", tiebreak_node)             
        tiebreak_trigger = 0
        for node in component_df.index:
            component_weight = 0
            component_weight_total = 0 
            for tree in df_transpose.index:
                component_weight = df_transpose.at[tree, node][1]
                if component_weight != .5:
                    if component_weight > .5:
                        component_weight = 1
                    else:
                        component_weight = 0
                else:
                    if tiebreak_node == 'None':  # assign every node in the tie with .5 status
                        component_weight = .5
                    else: # compare the component number of the tiebreak node to the current node
                        tiebreak_component = df_transpose.at[tree, tiebreak_node][0]
                        tiebreak_trigger += 1 
                        if df_transpose.at[tree, node][0] == tiebreak_component:
                            component_weight = 1
                        else:
                            component_weight = 0
                component_weight_total += component_weight
            status_list.append(100 * (component_weight_total / len(df_transpose.index)))
        print("tiebreak triggered :", tiebreak_trigger/16, " times")
        return status_list

    else: 
        for node in component_df.index:
            component_weight = 0 
            for tree in df_transpose.index:
                component_weight += df_transpose.at[tree, node][1]
            
            status_list.append(100 * (component_weight / len(df_transpose.index)))
       
        return status_list


def add_c0_pct_and_outcomes(tree_name, balanced_h5, component_df, tiebreak_node, weighted_status_flag):
    df_transpose = component_df.T

    c0_pct = calc_weighted_status(component_df, df_transpose, tiebreak_node, weighted_status_flag)

    ## counts the number of times each vertex is in c0 across each tree file -- works properly
    ## This line was how status was calculated before implementing the weighting and .5 tiebreak status stuff
 #   c0_pct = [100 * float(len(df_transpose.loc[df_transpose[i] == 0]) / len(df_transpose[i])) for i in component_df.index]

    df_dict_temp = {
        "% C0": c0_pct
    }
    
    mapping = list(balanced_h5['mapping_to_original'])
    df_dict_temp["Vert ID"] = [mapping[i] for i in component_df.index]
    assert(len(mapping) == len(component_df.index))
    print("ATTACHING OUTCOMES?")  
    if 'tree_bias_score' in balanced_h5.attrs:
        print("YES")
        outcomes = list(balanced_h5['outcomes'])
        df_dict_temp["outcome"] = outcomes
        assert(len(mapping) == len(outcomes))
    else:
        print("No bias score: Possibly a redflag? Dataset: ", balanced_h5.attrs['dataset'])
    df = pd.DataFrame(df_dict_temp) ### creates dataframe with status, node ID, and outcomes
    return df


