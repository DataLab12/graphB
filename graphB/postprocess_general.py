import subprocess
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from datetime import datetime
from dataset_paths import (
    get_config_path,
    get_output_file_path,
    print_timing_output,
    get_common_config_details,
    get_yaml_config_obj_by_key_tuple,
)
from df_creation import postprocess_vertex_df
from plot_creation import (
    postprocess_tree_bias_vs_c0,
    postprocess_vertex_status_vs_id,
)
from make_timing_dfs import create_write_filename, create_timing_results


def postprocess_locally(config_obj):
    postprocess_start = datetime.now()
    output_type = config_obj["machine"]
    print("-------------------- Config Object --------------------")
    print(config_obj)
    print("-------------------- End Config Object --------------------")
    if config_obj["postprocess"]:
        print("Creating at least one thing.")
        if config_obj["dataframes"]["vertex_df"]:
            postprocess_vertex_df(config_obj)
        if config_obj["plots"]["tree_bias_vs_c0"]:
            if config_obj["has_labels"]:
                postprocess_tree_bias_vs_c0(config_obj)
            else:
                print("You can't create a bias vs c0 graph: Your data has no labels.")
        if config_obj["plots"]["vertex_status_vs_id"]:
            postprocess_vertex_status_vs_id(config_obj)

    print_timing_output(
        "TOTAL_POSTPROCESS_TIME: (hh:mm:ss.ms)",
        datetime.now() - postprocess_start,
        output_type,
    )
    if output_type == "current":
        output_file = [get_output_file_path(config_obj)]
        timing_filename = create_write_filename(output_file)
        create_timing_results(output_file, timing_filename)


def submit_postprocess_LEAP_job(config_obj, process_jobID):
    (
        dataset,
        data_subset_type,
        matrix_name,
        num_trees,
        tree_type,
        parallelism,
    ) = get_common_config_details(config_obj)
    component_no = config_obj["component_no"]
    LEAP_output = None
    if config_obj["parallelism"] == "spark":
        print("Submitting postprocess job on LEAP using Spark")
        LEAP_output = subprocess.run(
            [
                "./wrapper_postprocess_general.sh",
                dataset,
                data_subset_type,
                matrix_name,
                str(component_no),
                str(process_jobID),
                num_trees,
                tree_type,
                parallelism,
            ],
            stdout=subprocess.PIPE,
        ).stdout.decode("utf-8")
    else:
        print("Submitting postprocess job on LEAP (non-Spark).")
        LEAP_output = subprocess.run(
            [
                "./wrapper_postprocess_general.sh",
                dataset,
                data_subset_type,
                matrix_name,
                str(component_no),
                str(process_jobID),
                num_trees,
                tree_type,
                parallelism,
            ],
            stdout=subprocess.PIPE,
        ).stdout.decode("utf-8")
    job_ID = int(LEAP_output.split()[-1])
    return job_ID


if __name__ == "__main__":
    print("Running postprocess main with args: ", sys.argv)
    dataset = str(sys.argv[1])
    data_subset_type = str(sys.argv[2])
    matrix_name = str(sys.argv[3])
    component_no = int(sys.argv[4])
    process_jobID = int(sys.argv[5])
    config_obj = get_yaml_config_obj_by_key_tuple(
        dataset, data_subset_type, matrix_name
    )
    postprocess_locally(config_obj)
