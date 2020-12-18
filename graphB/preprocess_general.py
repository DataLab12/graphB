import numpy as np
import pandas as pd
import scipy.sparse as sp
import pickle
import h5py
import os
import sys
import subprocess

import networkx as nx
from datetime import datetime

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from dataset_paths import (
    get_full_h5_path,
    print_timing_output,
    get_raw_dataset_csv_path,
    get_yaml_config_obj_by_key_tuple,
)
from constants import CONFIG_BASE


def order_components_descending(labels):
    comp_labels, counts = np.unique(labels, return_counts=True)
    dict_hist = dict(zip(comp_labels, counts))
    sorted_keys_list = sorted(dict_hist, key=dict_hist.get, reverse=True)
    labels = [sorted_keys_list.index(element) for element in labels]
    return labels


def get_full_unsym_csr_adj_matrix_and_possibly_outcomes_from_csv(config_obj):
    output_type = config_obj["machine"]
    edges_csv_path = (
        get_raw_dataset_csv_path(config_obj) + "_edges.csv"
    )  # Expects: From Node ID, To Node ID, Edge Weight
    users_csv_path = (
        get_raw_dataset_csv_path(config_obj) + "_users.csv"
    )  # Expects: Node ID, User ID, Label (optional)
    print("Attempting to read the following CSV's:")
    print("Edges: ", edges_csv_path)
    print("Users: ", users_csv_path)
    csr_adj_matrix = None
    users_df = None
    if os.path.isfile(edges_csv_path) and os.path.isfile(users_csv_path):
        data_df = pd.read_csv(edges_csv_path)
        start_matrix = datetime.now()
        row_ind = data_df.iloc[:, [0]]
        col_ind = data_df.iloc[:, [1]]
        data = data_df.iloc[:, [2]]

        row_vertices = data_df.iloc[:, [0]].max()
        col_vertices = data_df.iloc[:, [1]].max()
        max_vertices = int(max(row_vertices.values, col_vertices.values)) + 1

        csr_adj_matrix = sp.csr_matrix(
            (
                data.values.flatten(),
                (row_ind.values.flatten(), col_ind.values.flatten()),
            ),
            shape=(max_vertices, max_vertices),
        )
        print_timing_output(
            "MATRIX_CREATE_TIME: (hh:mm:ss.ms)",
            datetime.now() - start_matrix,
            output_type,
        )
        users_df = pd.read_csv(users_csv_path)
    else:
        print(
            "Error creating matrices from edges and users files. Please check the paths and filenames and make sure they are correct."
        )
    return csr_adj_matrix, users_df


def create_full_h5(config_obj):
    (
        csr_adj_matrix,
        users,
    ) = get_full_unsym_csr_adj_matrix_and_possibly_outcomes_from_csv(config_obj)
    G_pre_symm = nx.from_scipy_sparse_matrix(csr_adj_matrix)
    csr_adj_matrix = symmetricize(csr_adj_matrix)
    set_all_diag_to_zero(csr_adj_matrix)
    num_connected_components, labels = sp.csgraph.connected_components(
        csr_adj_matrix, return_labels=True
    )  # returns a list of the connected components with each one given a label. i.e. 0,1,2, etc.
    print("number of connected components: ", num_connected_components)
    G = nx.from_scipy_sparse_matrix(csr_adj_matrix)
    connected_comps = [
        c for c in sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
    ]
    comp_labels, counts = np.unique(labels, return_counts=True)
    dict_hist = dict(zip(comp_labels, counts))
    labels = order_components_descending(labels)
    comp_labels, counts = np.unique(labels, return_counts=True)
    dict_hist = dict(zip(comp_labels, counts))
    if dict_hist[0] < config_obj["min_component_size"]:
        print(
            "**** Largest component is not as big as minimum component size specified in 0.yaml, no sym h5s were made. ****"
        )
    else:
        print("Writing component 0")
        write_full_h5(connected_comps[0], config_obj, 0, True, labels, users)


def get_neighbors(vertex_number, graph_adj_matrix):
    neighbors = []
    if isinstance(graph_adj_matrix, np.ndarray):
        neighbors = [
            index
            for index, adjacency in enumerate(graph_adj_matrix[vertex_number])
            if adjacency != 0
        ]
    else:
        neighbors = list(
            np.split(graph_adj_matrix.indices, graph_adj_matrix.indptr)[
                vertex_number + 1 : vertex_number + 2
            ][0]
        )  # gets a list of neighbors of vertex <vertex_number>
    return neighbors


def write_full_h5(
    nx_connected_comp_graph, config_obj, component_no, is_symmetric, labels, users
):
    map_to_node_id = None
    if labels:
        map_to_node_id = [
            index
            for index, element in enumerate(labels)
            if int(element) == component_no
        ]
        component_no = int(component_no)
    else:
        map_to_node_id = [i for i in range(csr_adj_matrix.shape[0])]
        component_no = "full"
    full_h5_path = None
    full_h5_path = get_full_h5_path(config_obj)

    create_if_not_exists(full_h5_path)
    try:
        f = h5py.File(full_h5_path + str(component_no) + ".h5", "w")
        csr_adj_matrix = nx.to_scipy_sparse_matrix(
            nx_connected_comp_graph, nodelist=map_to_node_id
        )
        create_matrix_h5_file(f, csr_adj_matrix)
        f.attrs["dataset"] = config_obj["dataset"]
        f.attrs["data_subset_type"] = config_obj["data_subset_type"]
        f.attrs["matrix_name"] = config_obj["matrix_name"]
        f.attrs["component_no"] = component_no
        num_vertices = csr_adj_matrix.shape[0]
        grp = f.create_group("full_neighbors_list")
        progress_indicator = int(num_vertices / 20)
        print("Getting neighbors list.")
        start_neighbors = datetime.now()
        for i in range(num_vertices):
            if progress_indicator != 0 and num_vertices % progress_indicator == 0:
                print("Percent done: ", (i / num_vertices) * 100)
            grp.create_dataset(str(i), data=get_neighbors(i, csr_adj_matrix))
        print(
            "Neighbors List Acquired, took: (hh:mm:ss.ms) {}".format(
                datetime.now() - start_neighbors
            )
        )
        f.create_dataset("mapping_to_original", data=map_to_node_id)

        node_ids_subset = users[["Node ID"]]
        user_ids_subset = users[["User ID"]]
        node_ids = [x for x in node_ids_subset.values]
        user_ids = [x for x in user_ids_subset.values]
        f.create_dataset("node_ids", data=node_ids)

        dt = h5py.special_dtype(vlen=str)
        ds = f.create_dataset("user_ids", (len(user_ids),), dtype=dt)
        for i in range(len(user_ids)):
            ds[i] = user_ids[i]

        if len(users.columns) > 2 and users.columns[2] == "Label":
            create_outcomes_map(users, f, map_to_node_id)

        f.attrs["is_symmetric"] = is_symmetric
    finally:
        f.close()
    print(
        "Saved full h5: ",
        "(",
        config_obj["dataset"],
        ", ",
        config_obj["data_subset_type"],
        ", ",
        config_obj["matrix_name"],
        ", ",
        component_no,
        ") - symmetric: ",
        is_symmetric,
    )
    print("to: ", full_h5_path)


def create_outcomes_map(users, h5_file, map_to_node_id):
    f = h5_file
    users_dict = dict()
    outcomes_map = list()

    user_nodes = list(users["Node ID"])
    user_labels = list(users["Label"])

    for item in range(len(user_nodes)):
        users_dict.setdefault(user_nodes[item], user_labels[item])

    for key in map_to_node_id:
        if key in users_dict:
            outcomes_map.append(users_dict[key])

    f.create_dataset("outcomes", data=outcomes_map)


def preprocess_locally(config_obj):
    preprocess_start = datetime.now()
    output_type = config_obj["machine"]
    print("Preprocessing on: ", config_obj["machine"])
    if config_obj["preprocess"]:
        print("Making a symmetric full H5.")
        sym_start_time = datetime.now()
        create_full_h5(config_obj)
        print_timing_output(
            "SYM_MATRIX_CREATE_TIME: (hh:mm:ss.ms)",
            datetime.now() - sym_start_time,
            output_type,
        )
    else:
        print("Preprocess option not selected. Not making a symmetric full H5.")
    print("---------- Done making symmetric full H5 (if one was made)")
    print_timing_output(
        "TOTAL_PREPROCESS_TIME: (hh:mm:ss.ms)",
        datetime.now() - preprocess_start,
        output_type,
    )
    return 0


def submit_preprocess_LEAP_job(config_obj):
    print("Submitting preprocess job on LEAP")
    dataset = config_obj["dataset"]
    data_subset_type = config_obj["data_subset_type"]
    matrix_name = config_obj["matrix_name"]
    component_no = config_obj["component_no"]
    LEAP_output = subprocess.run(
        [
            "./wrapper_preprocess_general.sh",
            dataset,
            data_subset_type,
            matrix_name,
            str(component_no),
        ],
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8")
    job_ID = int(LEAP_output.split()[-1])
    return job_ID


def create_matrix_h5_file(g, csr_m):
    g.create_dataset("data", data=csr_m.data)
    g.create_dataset("indptr", data=csr_m.indptr)
    g.create_dataset("indices", data=csr_m.indices)
    g.attrs["shape"] = csr_m.shape


def create_if_not_exists(directory_to_possibly_create):
    if not os.path.exists(directory_to_possibly_create):
        os.makedirs(directory_to_possibly_create)


def symmetricize(data_matrix):
    if (data_matrix != data_matrix.transpose()).nnz > 0:  # data matrix is not symmetric
        data_matrix = (data_matrix + data_matrix.transpose()).sign()
    return data_matrix


def set_all_diag_to_zero(csr_m):
    csr_m.setdiag(0)


def save_obj(obj, name):
    with open("Preprocessed_Data/" + name + ".pkl", "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open("Preprocessed_Data/" + name + ".pkl", "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    print("Running preprocess main with args: ", sys.argv)
    dataset = str(sys.argv[1])
    data_subset_type = str(sys.argv[2])
    matrix_name = str(sys.argv[3])
    config_obj = get_yaml_config_obj_by_key_tuple(
        dataset, data_subset_type, matrix_name
    )
    preprocess_locally(config_obj)
