from pathlib import Path
import os
import h5py
from scipy.sparse import csr_matrix
import logging
import yaml


def create_if_not_exists(directory_to_possibly_create):
    if not os.path.exists(directory_to_possibly_create):
        os.makedirs(directory_to_possibly_create)


def get_common_config_details(config_obj):
    dataset = config_obj["dataset"]
    data_subset_type = config_obj["data_subset_type"]
    matrix_name = config_obj["matrix_name"]
    num_trees = str(config_obj["num_trees"])
    tree_type = str(
        [item for item in config_obj["tree_type"] if config_obj["tree_type"][item]][0]
    )
    parallelism = config_obj["parallelism"]

    return dataset, data_subset_type, matrix_name, num_trees, tree_type, parallelism


def get_output_file_path(config_obj):
    (
        dataset,
        data_subset_type,
        matrix_name,
        num_trees,
        tree_type,
        parallelism,
    ) = get_common_config_details(config_obj)
    machine = config_obj["machine"]
    log_directory = (
        "../data-" + dataset + "/Logfiles/" + data_subset_type + "_" + matrix_name + "/"
    )
    create_if_not_exists(log_directory)
    output_path = (
        log_directory
        + num_trees
        + tree_type
        + "_"
        + parallelism
        + "_"
        + machine
        + "_logs.txt"
    )

    return output_path


def get_raw_dataset_csv_path(config_obj):
    dataset_path = None
    if config_obj["machine"] == "current":
        dataset_path = (
            str(Path(__file__).parents[1])
            + "/data-"
            + config_obj["dataset"]
            + "/Input_Data/"
            + config_obj["data_subset_type"]
            + "_"
            + config_obj["matrix_name"]
        )
    elif config_obj["machine"] == "LEAP":
        dataset_path = (
            str(Path(__file__).parents[1])
            + "/data-"
            + config_obj["dataset"]
            + "/Input_Data/"
            + config_obj["data_subset_type"]
            + "_"
            + config_obj["matrix_name"]
        )
    return dataset_path


def get_config_path(dataset, data_subset_type, matrix_name):
    config_path = (
        str(Path(__file__).parents[0])
        + "/configs/"
        + dataset
        + "_"
        + data_subset_type
        + "_"
        + matrix_name
        + ".yaml"
    )
    return config_path


def get_yaml_config_obj_by_key_tuple(dataset, data_subset_type, matrix_name):
    # Example parameter set: "example1", "regular", "regular"
    config_path = get_config_path(dataset, data_subset_type, matrix_name)
    print("config_path: ", config_path)
    config_obj = None
    with open(config_path, "r") as stream:
        try:
            config_obj = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
    return config_obj


def get_full_h5_path(config_obj, local_override=False):
    dataset = config_obj["dataset"]
    parent_dir = None
    if config_obj["machine"] == "current":
        print("Machine: current")
        parent_dir = str(Path(__file__).parents[1]) + "/data-" + dataset + "/Data/"
    elif config_obj["machine"] == "LEAP":
        if config_obj["parallelism"] == "spark" and not local_override:
            print("Machine: LEAP, parallelism: Spark (no override)")
            parent_dir = str(Path(__file__).parents[1]) + "/data-" + dataset + "/Data/"
        else:
            print("Machine: LEAP, parallelism: Not spark (or override)")
            parent_dir = str(Path(__file__).parents[1]) + "/data-" + dataset + "/Data/"
    H5_PATH = (
        parent_dir
        + config_obj["data_subset_type"]
        + "_"
        + config_obj["matrix_name"]
        + "/"
    )
    print("Path: ", H5_PATH)
    return H5_PATH


def get_balanced_h5_path(config_obj, local_override=False):
    (
        dataset,
        data_subset_type,
        matrix_name,
        num_trees,
        tree_type,
        parallelism,
    ) = get_common_config_details(config_obj)
    BALANCED_H5_PATH = None
    if config_obj["machine"] == "current":
        BALANCED_H5_PATH = (
            str(Path(__file__).parents[1])
            + "/data-"
            + dataset
            + "/Data/"
            + data_subset_type
            + "_"
            + matrix_name
            + "/"
            + tree_type
            + "_trees"
            + "/"
        )
    elif config_obj["machine"] == "LEAP":
        if (
            config_obj["parallelism"] == "spark" and not local_override
        ):  # local_override should be false
            BALANCED_H5_PATH = (
                str(Path(__file__).parents[1])
                + "/data-"
                + dataset
                + "/Data/"
                + data_subset_type
                + "_"
                + matrix_name
                + "/"
                + tree_type
                + "_trees"
                + "/"
            )
        else:
            BALANCED_H5_PATH = (
                str(Path(__file__).parents[1])
                + "/data-"
                + dataset
                + "/Data/"
                + data_subset_type
                + "_"
                + matrix_name
                + "/"
                + tree_type
                + "_trees"
                + "/"
            )
    create_if_not_exists(BALANCED_H5_PATH)
    return BALANCED_H5_PATH


def get_full_csr_adj(config_obj, local_override=False):
    matrix_file_path = (
        get_full_h5_path(config_obj, local_override)
        + str(config_obj["component_no"])
        + ".h5"
    )
    mat = None
    print("Getting full sym csr adj from: ", matrix_file_path)
    f = h5py.File(matrix_file_path, "r")
    try:
        mat = csr_matrix(
            (f["data"][:], f["indices"][:], f["indptr"][:]), f.attrs["shape"]
        )
    finally:
        f.close()
    return mat


def get_balanced_csr_adj(config_obj, tree, local_override=False):
    return get_balanced_or_tree_csr_adj(
        config_obj, "csr_bal_adj_matrix", tree, local_override
    )


def get_tree_csr_adj(config_obj, tree, local_override=False):
    return get_balanced_or_tree_csr_adj(
        config_obj, "csr_st_adj_matrix", tree, local_override
    )


def get_balanced_or_tree_csr_adj(config_obj, bal_or_st, tree, local_override=False):
    matrix_file_path = get_balanced_h5_path(config_obj, local_override) + tree
    mat = None
    f = h5py.File(matrix_file_path, "r")
    g = f[bal_or_st]
    try:
        mat = csr_matrix(
            (g["data"][:], g["indices"][:], g["indptr"][:]), g.attrs["shape"]
        )
    finally:
        f.close()
    return mat


def get_postprocess_folder_general(config_obj):
    (
        dataset,
        data_subset_type,
        matrix_name,
        num_trees,
        tree_type,
        parallelism,
    ) = get_common_config_details(config_obj)
    postprocess_type_dir = None
    if config_obj["machine"] == "current":
        postprocess_type_dir = (
            str(Path(__file__).parents[1])
            + "/data-"
            + dataset
            + "/Output_Data/graphB/"
            + data_subset_type
            + "_"
            + matrix_name
            + "/"
        )
    elif config_obj["machine"] == "LEAP":
        postprocess_type_dir = (
            str(Path(__file__).parents[3])
            + "/data-"
            + dataset
            + "/Output_Data/graphB/"
            + data_subset_type
            + "_"
            + matrix_name
            + "/"
        )
    create_if_not_exists(postprocess_type_dir)
    return postprocess_type_dir


def print_timing_output(time_label, timestamp, output_type):
    if output_type == "current":
        logging.info(time_label + "%s" % timestamp)
    elif output_type == "LEAP":
        print(time_label + " ", timestamp)
