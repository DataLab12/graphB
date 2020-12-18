import sys
import yaml
import logging

from os.path import dirname, abspath, sep
from pathlib import Path

from constants import CONFIG_BASE

from preprocess_wrapper import submit_preprocess_job
from process_wrapper import submit_process_job
from postprocess_wrapper import submit_postprocess_job
from dataset_paths import get_output_file_path
from TimerManager import TimerManager

sys.setrecursionlimit(1000000000)


def get_yaml_config_obj_by_index(config_file_option):
    config_file_options_tuple_list = get_all_config_file_options()
    config_file_object = get_yaml_config_obj_by_key_tuple(
        *config_file_options_tuple_list[config_file_option]
    )
    return config_file_object


def get_yaml_config_obj_by_key_tuple(dataset, data_subset_type, matrix_name):
    # Example parameter set: "example1", "regular", "regular", 0
    config_path = (
        CONFIG_BASE + dataset + "_" + data_subset_type + "_" + matrix_name + ".yaml"
    )
    return get_yaml_config_obj_by_path(config_path)


def get_yaml_config_obj_by_path(config_path):
    config_obj = None
    with open(config_path, "r") as stream:
        try:
            config_obj = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config_obj


# def get_all_config_file_objs():
# 	config_file_options_tuple_list = get_all_config_file_options()
# 	config_file_obj_list = []
# 	for tup in config_file_options_tuple_list: # tup: (dataset, data_subset_type, matrix_name, component_no)
# 		config_obj = get_yaml_config_obj_by_key_tuple(*tup)
# 		config_file_obj_list.append(config_obj)
# 	return config_file_obj_list


def get_all_config_file_options():
    config_paths_list = [str(file) for file in list(Path(CONFIG_BASE).glob("*.yaml"))]
    option_keys_tuple_list = []
    for config_path in config_paths_list:
        option_keys_tuple = parse_config_path(config_path)
        option_keys_tuple_list.append(option_keys_tuple)
    return option_keys_tuple_list


def parse_config_path(config_path):
    # Example config_path: '/Users/jm/graphB/configs/example1/regular/regular/0.yaml'
    key_list = config_path.split(sep)[-1].split("_")
    dataset = key_list[0]
    data_subset_type = key_list[1]
    matrix_name = key_list[2].split(".")[0]
    return (dataset, data_subset_type, matrix_name)


def set_output_location(config_obj, output_path):
    if config_obj["machine"] == "current":
        logging.basicConfig(filename=output_path, filemode="w", level=logging.DEBUG)
        print("\nStarting to write timing logs to file at: ", output_path, "\n")
    elif config_obj["machine"] == "LEAP":
        print("\nStarting to write all output to file at: ", output_path, "\n")
        sys.stdout = open(output_path, "w")


def execute_jobs_by_config_file_index(config_file_option):
    config_obj = get_yaml_config_obj_by_index(config_file_option)
    output_path = get_output_file_path(config_obj)
    set_output_location(config_obj, output_path)
    execute_jobs_by_config_file(config_obj, True)


def execute_jobs_by_config_file(config_obj, index_run_flag):
    # jobID's: 0 means do it on current machine, None means don't do it (already done or not requested), any other positive integer means do it on LEAP
    if not index_run_flag:
        output_path = get_output_file_path(config_obj)
        set_output_location(config_obj, output_path)
    print("******************** Starting Preprocessing Step  ******************** ")
    preprocess_jobID = submit_preprocess_job(config_obj)
    print(
        "******************** Finished Preprocessing Step (jobID: ",
        preprocess_jobID,
        "); Starting Process Step ******************** ",
    )
    process_jobID = submit_process_job(config_obj, preprocess_jobID)
    print(
        "******************** Finished Processing Step (jobID: ",
        process_jobID,
        "); Starting Postprocess Step ********************** ",
    )
    postprocess_jobID = submit_postprocess_job(config_obj, process_jobID)
    print(
        "******************** Finished Postprocessing Step (jobID: ",
        postprocess_jobID,
        "). Exiting. *******************************",
    )


if __name__ == "__main__":
    TimerManager.addTimer("global")
    TimerManager.startTimerX(0)

    print("--------------------------------------")
    print("Arguments: ", sys.argv)
    if len(sys.argv) == 1:
        config_file_options_list = get_all_config_file_options()
        print(
            "No config file selected. List of config files you can use (pass the index as the first argument):"
        )
        for index, config_file_option in enumerate(config_file_options_list):
            print(index, " ---> ", config_file_option)
        print()
        print("Legend: (dataset, data_subset_type, matrix_name)")
    else:
        if str(sys.argv[1]).isdigit():
            config_file_option = int(sys.argv[1])
            print(
                "Integer detected as first run.py parameter: using config file corresponding to that index: ",
                config_file_option,
            )
            execute_jobs_by_config_file_index(config_file_option)
        else:
            print(
                "Integer not detected as first run.py parameter. Will assume it's a path: ",
                str(sys.argv[1]),
            )
            print("Example path: configs/example1/regular/regular/0.yaml")
            config_path = str(sys.argv[1])
            config_obj = get_yaml_config_obj_by_path(config_path)
            execute_jobs_by_config_file(config_obj, False)

    print("--------------------------------------")
