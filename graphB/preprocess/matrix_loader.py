import scipy.sparse as sp
from pathlib import Path
import os.path
import sys
import pandas as pd
sys.path.append("..")
import csv
import numpy as np

from dataset_paths import get_raw_dataset_path, get_raw_dataset_subset_path, get_raw_dataset_csv_path

def get_full_unsym_csr_adj_matrix_and_possibly_outcomes_from_csv(config_obj):
    edges_csv_path = get_raw_dataset_csv_path(config_obj) + "_edges.csv" # Expects: From Node ID, To Node ID, Edge Weight
    users_csv_path = get_raw_dataset_csv_path(config_obj) + "_users.csv" # Expects: Node ID, User ID, Label (optional)
    print("Attempting to read the following CSV's:")
    print("Edges: ", edges_csv_path)
    print("Users: ", users_csv_path)
    csr_adj_matrix = None
    users_df = None
    if os.path.isfile(edges_csv_path) and os.path.isfile(users_csv_path):
        # we have labeled data - RZ: This checkes that the file paths and directories to the edges.csv and users.csv exists 
        # Might need to sort
        data_df = pd.read_csv(edges_csv_path) # RZ - this reads in the edges.csv file with all defult settings. 
        # RZ - make the data_df read in the 1st column as row ind, 2nd column as col_ind, 3rd column as data so that it can read in any column name. 
        # Changed the column names to have _'s because postgres does not know how to read and write column names with sapces. 
       
        row_ind = data_df.iloc[:,[0]] # RZ - this reads the data From Node ID column and makes a list
        col_ind = data_df.iloc[:,[1]]
        data = data_df.iloc[:,[2]]

        

        row_vertices = data_df.iloc[:,[0]].max() # finds the largest from node id
        col_vertices = data_df.iloc[:,[1]].max() # finds the largest to node id 
        
        max_vertices = int(max(row_vertices.values, col_vertices.values)) + 1
        
        # 
        csr_adj_matrix = sp.csr_matrix((data.values.flatten(), (row_ind.values.flatten(), col_ind.values.flatten())),shape=(max_vertices, max_vertices))      
 
        print('shape of created matrix', csr_adj_matrix.shape)
        # RZ- The output matrix will be sorted by row_ind value
        # Might need to sort
        users_df = pd.read_csv(users_csv_path) 
        # RZ- What is the purpose of performing these two steps. 
        print("Matrix:")
        print(csr_adj_matrix.toarray())
    else:
        # something went wrong
        print("Something went wrong!")
    return csr_adj_matrix, users_df
