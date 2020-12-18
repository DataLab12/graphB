import sys
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
from datetime import datetime

from dataset_paths import (
    get_balanced_h5_path,
    get_postprocess_folder_general,
    get_full_csr_adj,
    get_balanced_csr_adj,
    get_tree_csr_adj,
    get_raw_dataset_csv_path,
    get_common_config_details,
    print_timing_output,
)
from TimerManager import TimerManager

sys.path.append("..")


def get_balanced_file_list(config_obj, local_override=False):
    BALANCED_DIR = get_balanced_h5_path(config_obj, local_override)
    balanced_file_list = [
        f
        for f in listdir(BALANCED_DIR)
        if isfile(join(BALANCED_DIR, f))
        if f != ".DS_Store"
    ]
    balanced_file_list.sort()
    print("Tree list Length: ", len(balanced_file_list))
    return balanced_file_list


def create_if_not_exists(directory_to_possibly_create):
    if not os.path.exists(directory_to_possibly_create):
        os.makedirs(directory_to_possibly_create)


def get_file_tag(config_obj):
    (
        dataset,
        data_subset_type,
        matrix_name,
        num_trees,
        tree_type,
        parallelism,
    ) = get_common_config_details(config_obj)
    file_tag = num_trees + tree_type + "_" + parallelism
    if config_obj["has_labels"]:
        if config_obj["weighted_status"]:
            file_tag = file_tag + "_weighted_outcomes_"
        elif config_obj["tiebreak_node"] != "None":
            file_tag = (
                file_tag
                + "_unweighted_tiebreakNode"
                + str(config_obj["tiebreak_node"])
                + "_outcomes_"
            )
        else:
            file_tag = file_tag + "_unweighted_outcomes_"
    else:
        if config_obj["weighted_status"]:
            file_tag = file_tag + "_weighted_no_outcomes_"
        elif config_obj["tiebreak_node"] != "None":
            file_tag = (
                file_tag
                + "_unweighted_tiebreakNode"
                + str(config_obj["tiebreak_node"])
                + "_no_outcomes_"
            )
        else:
            file_tag = file_tag + "_unweighted_no_outcomes_"
    return file_tag


########################################################################
### Calculate vertex dfs
########################################################################


def postprocess_vertex_df(config_obj, dont_remake_override=False):
    (
        dataset,
        data_subset_type,
        matrix_name,
        num_trees,
        tree_type,
        parallelism,
    ) = get_common_config_details(config_obj)
    output_folder = get_postprocess_folder_general(config_obj)
    output_type = config_obj["machine"]
    file_tag = get_file_tag(config_obj)
    FULL_DF_PATH = output_folder + file_tag + "_vertex_df.pkl"
    vertex_df = None
    print("-------- Entering Post-Process Vertex DF --------")
    if (
        not isfile(FULL_DF_PATH) or config_obj["postprocess"]
    ) and not dont_remake_override:
        print("-------- Creating Vertex DF --------")
        # if (it's not a file or we want to remake it) AND we're not calling this function from a plotting fn, table fn, etc...
        to_be_df_dict = None
        trees_list = get_balanced_file_list(config_obj, True)
        if parallelism == "parallel" or parallelism == "spark":
            num_cores = mp.cpu_count()
            print(
                "Creating vertex df (parallel: ",
                num_cores,
                " cores):",
                dataset,
                ", ",
                data_subset_type,
                ", ",
                matrix_name,
                ") ",
            )
            vertex_df_start = datetime.now()
            df_tup_list = Parallel(n_jobs=num_cores)(
                delayed(get_per_tree_vertex_dict_tup)(tree, config_obj)
                for tree in trees_list
            )
            to_be_df_dict = {tup[0]: tup[1] for tup in df_tup_list}
            print("Finished base, adding component and outcome columns.")
        elif parallelism == "serial":
            print(
                "Creating vertex df (serial):",
                dataset,
                ", ",
                data_subset_type,
                ", ",
                matrix_name,
                ") ",
            )
            vertex_df_start = datetime.now()
            to_be_df_dict = {
                tree: get_per_tree_vertex_dict(tree, config_obj) for tree in trees_list
            }
            print("Finished base, adding component and outcome columns.")
        vertex_df = create_vertex_df_from_vertex_dict(
            to_be_df_dict, config_obj, trees_list, FULL_DF_PATH
        )
        print_timing_output(
            "VERTEX_DF_TIME: (hh:mm:ss.ms)",
            datetime.now() - vertex_df_start,
            output_type,
        )
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
        print(
            "No file in map_csv path. Ignore this if your users do not have any mapping."
        )
        users_map_df = None
        ignore = True
    return users_map_df, ignore


def create_vertex_df_from_vertex_dict(
    to_be_df_dict, config_obj, trees_list, FULL_DF_PATH
):
    print("Creating components dict.")
    try:
        components_dict = {
            tree: to_be_df_dict[tree]["component_list"] for tree in trees_list
        }
        component_df = pd.DataFrame(components_dict)
        component_dict_with_weights = {
            tree: to_be_df_dict[tree]["component_list_with_tuples"]
            for tree in trees_list
        }
        component_weights_df = pd.DataFrame(component_dict_with_weights)
    except:
        print("tree without component list found, moving to next.")

    balanced_h5_file = get_balanced_h5_path(config_obj, True) + trees_list[0]
    try:
        balanced_h5 = h5py.File(balanced_h5_file, "r")
        print("Adding c0 pct (and outcomes if applicable).")
        vertex_df = add_c0_pct_and_outcomes(
            trees_list[0],
            balanced_h5,
            component_weights_df,
            config_obj["tiebreak_node"],
            config_obj["weighted_status"],
            config_obj["machine"],
        )
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
        balanced_h5 = h5py.File(balanced_h5_file, "r")
        row["component_list_with_tuples"] = list(
            balanced_h5["weighted_component_list"]
        )

        row["component_list"] = list(balanced_h5["component_list"])
        row["vertex_neighbor_amt_list"] = list(balanced_h5["vertex_neighbor_amt_list"])
        row["mean_tree_vertex_deg"] = balanced_h5.attrs["mean_tree_vertex_deg"]
        row["stdev_tree_vertex_deg"] = balanced_h5.attrs["stdev_tree_vertex_deg"]
        row["pendant_vertices_c0"] = balanced_h5.attrs["pendant_vertices_c0"]
        row["pendant_vertices_c1"] = balanced_h5.attrs["pendant_vertices_c1"]
        row["pendant_vertices_total"] = balanced_h5.attrs["pendant_vertices_total"]
        balanced_h5.close()
    except Exception as error:
        print(
            "Vertex DF error. The following tree is bad. ",
            tree,
            " - path: ",
            balanced_h5_file,
        )
        print("error: ", error)

    return row


def calc_weighted_status(
    component_df, df_transpose, tiebreak_node, weighted_status_flag
):
    status_list = []
    if not weighted_status_flag:
        print("running without weighted status, tiebreak node is:", tiebreak_node)
        tiebreak_trigger = 0
        for node in component_df.index:
            component_weight = 0
            component_weight_total = 0
            for tree in df_transpose.index:
                component_weight = df_transpose.at[tree, node][1]
                if component_weight != 0.5:
                    if component_weight > 0.5:
                        component_weight = 1
                    else:
                        component_weight = 0
                else:
                    if (
                        tiebreak_node == "None"
                    ):  # assign every node in the tie with .5 status
                        component_weight = 0.5
                        tiebreak_trigger += 1
                    else:  # compare the component number of the tiebreak node to the current node
                        tiebreak_component = df_transpose.at[tree, tiebreak_node][0]
                        tiebreak_trigger += 1
                        if df_transpose.at[tree, node][0] == tiebreak_component:
                            component_weight = 1
                        else:
                            component_weight = 0
                component_weight_total += component_weight
            status_list.append(100 * (component_weight_total / len(df_transpose.index)))
        print("tiebreak triggered :", tiebreak_trigger / len(component_df.index), " times")

        return status_list

    else:
        for node in component_df.index:
            component_weight = 0
            for tree in df_transpose.index:
                component_weight += df_transpose.at[tree, node][1]

            status_list.append(100 * (component_weight / len(df_transpose.index)))

        return status_list


def add_c0_pct_and_outcomes(
    tree_name,
    balanced_h5,
    component_df,
    tiebreak_node,
    weighted_status_flag,
    output_type,
):
    df_transpose = component_df.T
    start_status = datetime.now()
    c0_pct = calc_weighted_status(
        component_df, df_transpose, tiebreak_node, weighted_status_flag
    )
    print_timing_output(
        "CALC_STATUS_TIME: (hh:mm:ss.ms)", datetime.now() - start_status, output_type
    )
    df_dict_temp = {"% C0": c0_pct}

    mapping = list(balanced_h5["mapping_to_original"])
    df_dict_temp["Vert ID"] = [mapping[i] for i in component_df.index]
    assert len(mapping) == len(component_df.index)
    print("ATTACHING OUTCOMES?")
    if "tree_bias_score" in balanced_h5.attrs:
        print("YES")
        outcomes = list(balanced_h5["outcomes"])
        df_dict_temp["outcome"] = outcomes
        assert len(mapping) == len(outcomes)
    else:
        print(
            "No bias score: Possibly a redflag? Dataset: ", balanced_h5.attrs["dataset"]
        )
    df = pd.DataFrame(
        df_dict_temp
    )  ### creates dataframe with status, node ID, and outcomes
    TimerManager.stopTimerX(0)
    print_timing_output(
        "GLOBAL_TIME: (hh:mm:ss.ms)", str(TimerManager.getTimerXElapsed(0)), output_type
    )
    return df
