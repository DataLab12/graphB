import sys
import yaml

from os.path import dirname, abspath, sep
from pathlib import Path

from constants import CONFIG_BASE

from preprocess.preprocess_wrapper import submit_preprocess_job
from process.process_wrapper import submit_process_job
from postprocess.postprocess_wrapper import submit_postprocess_job

sys.setrecursionlimit(1000000000)

def get_yaml_config_obj_by_index(config_file_option):
	config_file_obj_list = get_all_config_file_objs()
	return config_file_obj_list[config_file_option]

def get_yaml_config_obj_by_key_tuple(dataset, data_subset_type, matrix_name, component_no):
	# Example parameter set: "example1", "regular", "regular", "0" (or 0, maybe)
	config_path = CONFIG_BASE + dataset + "/" + data_subset_type + "/" + matrix_name + "/" + str(component_no) + ".yaml"
	return get_yaml_config_obj_by_path(config_path)

def get_yaml_config_obj_by_path(config_path):
	config_obj = None
	with open(config_path, 'r') as stream:
	    try:
	    	config_obj = yaml.load(stream)
	    except yaml.YAMLError as exc:
	    	print(exc)
	return config_obj

def get_all_config_file_objs():
	config_file_options_tuple_list = get_all_config_file_options()
	config_file_obj_list = []
	for tup in config_file_options_tuple_list: # tup: (dataset, data_subset_type, matrix_name, component_no)
		config_obj = get_yaml_config_obj_by_key_tuple(*tup) # expands all arguments in tup and passes them as parameters to the function
		config_file_obj_list.append(config_obj)
	return config_file_obj_list

def get_all_config_file_options():
	config_paths_list = [str(file) for file in list(Path(CONFIG_BASE).glob('**/*.yaml'))] # traverse through whole config directory of config files and get all their paths
	option_keys_tuple_list = []
	for config_path in config_paths_list:
		option_keys_tuple = parse_config_path(config_path)
		option_keys_tuple_list.append(option_keys_tuple)
	return option_keys_tuple_list

def parse_config_path(config_path):
	# Example config_path: '/Users/jm/graphB/configs/example1/regular/regular/0.yaml'
    key_list = config_path.split(sep) 
    component_no = int(key_list[-1][0])
    matrix_name = key_list[-2]
    data_subset_type = key_list[-3]
    dataset = key_list[-4]
    return (dataset, data_subset_type, matrix_name, component_no)

def execute_jobs_by_config_file_index(config_file_option):
	config_obj = get_yaml_config_obj_by_index(config_file_option)
	execute_jobs_by_config_file(config_obj)

def execute_jobs_by_config_file(config_obj):
	# jobID's: 0 means do it on current machine, None means don't do it (already done or not requested), any other positive integer means do it on LEAP
	print("******************** Starting Preprocessing Step  ******************** ")
	preprocess_jobID = submit_preprocess_job(config_obj)
	print("******************** Finished Preprocessing Step (jobID: ", preprocess_jobID, "); Starting Process Step ******************** ")
	process_jobID = submit_process_job(config_obj, preprocess_jobID)
	print("******************** Finished Processing Step (jobID: ", process_jobID, "); Starting Postprocess Step ********************** ")
	postprocess_jobID = submit_postprocess_job(config_obj, process_jobID)
	print("******************** Finished Postprocessing Step (jobID: ", postprocess_jobID, "). Exiting. *******************************")

if __name__ == "__main__":
	print("--------------------------------------")
	print("Arguments: ", sys.argv)
	if len(sys.argv) == 1:
		config_file_options_list = get_all_config_file_options()
		print('No config file selected. List of config files you can use (pass the index as the first argument):')
		for index, config_file_option in enumerate(config_file_options_list):
			print(index, " ---> ", config_file_option)
		print()
		print('Legend: (dataset, data_subset_type, matrix_name, component_no)')
	else:
		if str(sys.argv[1]).isdigit():
			config_file_option = int(sys.argv[1])
			print("Integer detected as first run.py parameter: using config file corresponding to that index: ", config_file_option)
			execute_jobs_by_config_file_index(config_file_option)
		else:
			print("Integer not detected as first run.py parameter. Will assume it's a path: ", str(sys.argv[1]))
			print("Example path: configs/example1/regular/regular/0.yaml")
			config_path = str(sys.argv[1])
			config_obj = get_yaml_config_obj_by_path(config_path)
			execute_jobs_by_config_file(config_obj)

	print("--------------------------------------")
