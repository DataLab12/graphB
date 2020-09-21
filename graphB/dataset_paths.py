from pathlib import Path
import os
import h5py
from scipy.sparse import csr_matrix

def create_if_not_exists(directory_to_possibly_create):
  if not os.path.exists(directory_to_possibly_create):
    os.makedirs(directory_to_possibly_create)

def get_raw_dataset_path(dataset, config_obj):
    dataset_path = None
    if config_obj['machine'] == "current":
        dataset_path = str(Path(__file__).parents[1]) + "/data-" + dataset + "/Raw_Data/" + dataset + ".txt"
    elif config_obj['machine'] == "LEAP":
        dataset_path = str(Path(__file__).parents[3]) + "/data-" + dataset + "/Raw_Data/" + dataset + ".txt"
    return dataset_path

def get_raw_dataset_csv_path(config_obj):
    dataset_path = None
    if config_obj['machine'] == "current":
        dataset_path = str(Path(__file__).parents[1]) + "/data-" + config_obj['dataset'] + "/Raw_Data/" + config_obj['data_subset_type'] + "_" + config_obj['matrix_name']
    elif config_obj['machine'] == "LEAP":
        dataset_path = str(Path(__file__).parents[3]) + "/data-" + config_obj['dataset'] + "/Raw_Data/" + config_obj['data_subset_type'] + "_" + config_obj['matrix_name']
    return dataset_path

def get_config_path(dataset, data_subset_type, matrix_name, component_no):
    config_path = str(Path(__file__).parents[2]) + "/configs/" + dataset + "/" + data_subset_type + "/" + matrix_name + "/" + str(component_no) + ".yaml"
    return config_path

def get_matrix_names_for_type_and_dataset(config_obj):
    dataset = config_obj["dataset"]
    data_subset_type = config_obj["data_subset_type"]
    config_path = str(Path(__file__).parents[0]) + "/configs/" + dataset + "/" + data_subset_type + "/"
    dirlist = [ item for item in os.listdir(config_path) if os.path.isdir(os.path.join(config_path, item)) ]
    return dirlist

def get_raw_dataset_subset_path(dataset, data_subset_type, matrix_file_name, config_obj):
    dataset_path = None
    if config_obj['machine'] == "current":
        dataset_path = str(Path(__file__).parents[1]) + "/data-" + dataset + "/Raw_Data/" + data_subset_type + "/" + matrix_file_name + ".txt"
    elif config_obj['machine'] == "LEAP":
        dataset_path = str(Path(__file__).parents[3]) + "/data-" + dataset + "/Raw_Data/" + data_subset_type + "/" + matrix_file_name + ".txt"
    return dataset_path
    
def get_full_sym_h5_path(config_obj, local_override=False):
    return get_full_h5_path(config_obj, True, local_override)

def get_full_unsym_h5_path(config_obj, local_override=False):
    return get_full_h5_path(config_obj, False, local_override)

def get_full_h5_path(config_obj, symmetric, local_override=False):
    dataset = config_obj['dataset']
    parent_dir = None
    if config_obj['machine'] == "current":
        print("Machine: current")
        parent_dir = str(Path(__file__).parents[1]) + "/data-" + dataset + "/Input_Data/"
    elif config_obj['machine'] == "LEAP":
        if config_obj['parallelism'] == 'spark' and not local_override:
            print("Machine: LEAP, parallelism: Spark (no override)")
            parent_dir = str(Path(__file__).parents[1]) + "/data-" + dataset + "/Input_Data/"
        else:
            print("Machine: LEAP, parallelism: Not spark (or override)")
            parent_dir = str(Path(__file__).parents[3]) + "/data-" + dataset + "/Input_Data/"
    H5_PATH = parent_dir + config_obj['data_subset_type'] + "/" + config_obj['matrix_name']
    if symmetric:
        H5_PATH += "/sym/"
    else:
        H5_PATH += "/unsym/"
    print("Path: ", H5_PATH)
    return H5_PATH

def get_balanced_h5_path(config_obj, local_override=False):
    dataset = config_obj['dataset']
    data_subset_type = config_obj['data_subset_type']
    matrix_name = config_obj['matrix_name']
    component_no = config_obj['component_no']
    BALANCED_H5_PATH = None
    if config_obj['machine'] == "current":
        BALANCED_H5_PATH = str(Path(__file__).parents[1]) + "/data-" + dataset + "/Data/" + data_subset_type + "/" + matrix_name + "/" + str(component_no) + "/"
        # print("Branch 1")
    elif config_obj['machine'] == "LEAP":
        if config_obj['parallelism'] == 'spark' and not local_override: # local_override should be false
            BALANCED_H5_PATH = str(Path(__file__).parents[1]) + "/data-" + dataset + "/Data/" + data_subset_type + "/" + matrix_name + "/" + str(component_no) + "/"
            # print("Branch 2")
        else:
            BALANCED_H5_PATH = str(Path(__file__).parents[3]) + "/data-" + dataset + "/Data/" + data_subset_type + "/" + matrix_name + "/" + str(component_no) + "/"
            # print("Branch 3")
    create_if_not_exists(BALANCED_H5_PATH)
    # print("BALANCED_H5_PATH: ", BALANCED_H5_PATH)
    return BALANCED_H5_PATH

def get_full_csr_adj(config_obj, local_override=False):
    matrix_file_path = get_full_sym_h5_path(config_obj, local_override) + str(config_obj['component_no']) + ".h5"
    mat = None
    print("Getting full sym csr adj from: ", matrix_file_path)
    f = h5py.File(matrix_file_path, 'r')
    try:
        mat = csr_matrix((f['data'][:], f['indices'][:], f['indptr'][:]), f.attrs['shape'])
    finally:
        f.close()
    return mat

def get_balanced_csr_adj(config_obj, tree, local_override=False):
    return get_balanced_or_tree_csr_adj(config_obj, "csr_bal_adj_matrix", tree, local_override)

def get_tree_csr_adj(config_obj, tree, local_override=False):
    return get_balanced_or_tree_csr_adj(config_obj, "csr_st_adj_matrix", tree, local_override)

def get_balanced_or_tree_csr_adj(config_obj, bal_or_st, tree, local_override=False):
    matrix_file_path = get_balanced_h5_path(config_obj, local_override) + tree
    mat = None
    # print("Getting ", bal_or_st, " csr adj from: ", matrix_file_path)
    f = h5py.File(matrix_file_path, 'r')
    g = f[bal_or_st]
    try:
        mat = csr_matrix((g['data'][:], g['indices'][:], g['indptr'][:]), g.attrs['shape'])
    finally:
        f.close()
    return mat

def get_full_unsym_csr_adj(config_obj, local_override=False):
    matrix_file_path = get_full_unsym_h5_path(config_obj, local_override) + "full.h5"
    mat = None
    print("Getting full unsym csr adj from: ", matrix_file_path)
    f = h5py.File(matrix_file_path, 'r')
    try:
        mat = csr_matrix((f['data'][:], f['indices'][:], f['indptr'][:]), f.attrs['shape'])
    finally:
        f.close()
    return mat

def get_stats_folder(config_obj):
    return get_postprocess_folder_general(config_obj, "stats")

def get_df_folder(config_obj):
    return get_postprocess_folder_general(config_obj, "dfs")

def get_plots_folder(config_obj):
    return get_postprocess_folder_general(config_obj, "plots")

def get_tables_folder(config_obj):
    return get_postprocess_folder_general(config_obj, "tables")

def get_postprocess_folder_general(config_obj, postprocess_type):
    dataset = config_obj['dataset']
    postprocess_type_dir = None
    if config_obj['machine'] == "current":
        postprocess_type_dir = str(Path(__file__).parents[1]) + "/data-" + dataset + "/Output_Data/" + postprocess_type + "/"
    elif config_obj['machine'] == "LEAP":
        postprocess_type_dir = str(Path(__file__).parents[3]) + "/data-" + dataset + "/Output_Data/" + postprocess_type + "/"
    create_if_not_exists(postprocess_type_dir)
    return postprocess_type_dir
