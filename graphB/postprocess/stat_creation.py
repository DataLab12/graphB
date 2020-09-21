import sys
sys.path.append("..")

import networkx as nx
import gc
import multiprocessing as mp
import time
import statistics

import numpy as np
import os
import pickle
from os import listdir
from os.path import isfile, join, splitext, dirname, abspath
from joblib import Parallel, delayed

from dataset_paths import get_balanced_csr_adj, get_stats_folder
from postprocess.df_creation import get_balanced_file_list

def postprocess_all_stats(config_obj):
    postprocess_BEC_list(config_obj)
   
###########################
### BEC List
###########################

def balanced_matrix_comparison(config_obj, tree1, tree2):
    # read both matrices
    m1 = get_balanced_csr_adj(config_obj, tree1, True)
    m2 = get_balanced_csr_adj(config_obj, tree2, True)

    # subtract 1 from the other
    dif = m1 - m2

    # if nonzero > 0, return 0, else return 1
    result = 1
    if dif.getnnz() > 0:
        result = 0
    del m1
    del m2
    del dif
    gc.collect()
    return result

def create_BEC_matrix_row(config_obj, tree_row, trees_list):
    return [ 0 if tree_row == tree_col else balanced_matrix_comparison(config_obj, tree_row, tree_col) for tree_col in trees_list ] 

def create_BEC_matrix(config_obj):
    trees_list = get_balanced_file_list(config_obj, True)
    A = None
    start = time.time()
    if config_obj['parallelism'] == 'parallel' or config_obj['parallelism'] == 'spark':
        num_cores = mp.cpu_count()
        print("Creating BEC matrix (parallel: ", num_cores, " cores):", config_obj['dataset'], ", ", config_obj['data_subset_type'], ", ", config_obj['matrix_name'], ", ", config_obj['component_no'], ") ")
        pool = mp.Pool(processes=num_cores)
        A = [ pool.apply(create_BEC_matrix_row, args=(config_obj, tree_row, trees_list)) for tree_row in trees_list ]
        # print(results)
    elif config_obj['parallelism'] == 'serial':
        print("Creating BEC matrix (serial):", config_obj['dataset'], ", ", config_obj['data_subset_type'], ", ", config_obj['matrix_name'], ", ", config_obj['component_no'], ") ")

        # A = []
        # for tree_row in trees_list:
        #     z = []
        #     for tree_col in trees_list:
        #         if tree_row != tree_col:
        #             z.append(balanced_matrix_comparison(config_obj, tree_row, tree_col))
        #         else:
        #             z.append(0)
        #     A.append(z)

        # This compact double list comprehension below is equal to the logic above:
        # A = [ [ 0 if tree_row == tree_col else balanced_matrix_comparison(config_obj, tree_row, tree_col) for tree_col in trees_list ] for tree_row in trees_list ]
        A = [ create_BEC_matrix_row(config_obj, tree_row, trees_list) for tree_row in trees_list ]
    end = time.time()
    print("Time elapsed (seconds): ", end - start)
    return np.array(A)

def postprocess_BEC_list(config_obj):
    print("-------- Entering Post-Process BEC Histogram --------")

    STATS_FOLDER = get_stats_folder(config_obj)
    PKL = ".pkl"
    TXT = ".txt"
    FULL_FILE_PATH = STATS_FOLDER + config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_" + str(config_obj['component_no']) + "_BEC_Hist"
    CC_size_list = None

    # if BEC dict doesn't exist or recreate
    if (not isfile(FULL_FILE_PATH + PKL) or config_obj['postprocess_again']):
        BEC_matrix = create_BEC_matrix(config_obj)
        np.fill_diagonal(BEC_matrix, 0)
        G = nx.from_numpy_matrix(BEC_matrix)
        CC_size_list = [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]

        # pickle it
        with open(FULL_FILE_PATH + PKL, 'wb') as handle:
            pickle.dump(CC_size_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(FULL_FILE_PATH + TXT, "w") as text_file:
            print("Number of BECs: {}".format(len(CC_size_list)), file=text_file)
            mean = statistics.mean(CC_size_list)
            stdev = statistics.stdev(CC_size_list)
            print("Mean: {}".format(mean), file=text_file)
            print("Stdev: {}".format(stdev), file=text_file)
            print("BEC Histogram: {}".format(" ".join(str(x) for x in CC_size_list)), file=text_file)
    else:
        print("-------- Reading BEC Histogram --------")
        with open(FULL_FILE_PATH + PKL, 'rb') as handle:
            CC_size_list = pickle.load(handle)
    print("BEC Histogram: ")
    print(CC_size_list)
    print("Total BEC's: ", len(CC_size_list))
    return CC_size_list
