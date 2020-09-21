import subprocess
import sys
import yaml
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from dataset_paths import get_config_path
from postprocess.df_creation import postprocess_vertex_df, postprocess_tree_df, postprocess_all_dfs 
from postprocess.plot_creation import (postprocess_tree_bias_vs_c0, postprocess_vertex_status_vs_id, postprocess_all_plots, 
   postprocess_histograms)
from postprocess.table_creation import (postprocess_vertex_table, postprocess_tree_table, postprocess_all_tables, 
   postprocess_tree_corr_table)
from postprocess.stat_creation import postprocess_BEC_list, postprocess_all_stats

def get_yaml_config_obj_by_key_tuple(dataset, data_subset_type, matrix_name, component_no):
	# Example parameter set: "example1", "regular", "regular", "0" (or 0, maybe)
    config_path = get_config_path(dataset, data_subset_type, matrix_name, component_no)
    print("config_path: ", config_path)
    config_obj = None
    with open(config_path, 'r') as stream:
	    try:
	    	config_obj = yaml.load(stream)
	    except yaml.YAMLError as exc:
	    	print(exc)
    return config_obj

def postprocess_everything(config_obj):
    postprocess_all_dfs(config_obj)
    postprocess_all_plots(config_obj)
    postprocess_all_tables(config_obj)

def postprocess_locally(config_obj):
    print("-------------------- Config Object --------------------")
    print(config_obj)
    print("-------------------- End Config Object --------------------")
    if config_obj['all']:
        print("Postprocessing Everything")
        postprocess_everything(config_obj)
    elif config_obj['all_dfs'] or config_obj['all_plots'] or config_obj['all_tables']:
        if config_obj['all_dfs']:
            print("Postprocessing all DFS")
            postprocess_all_dfs(config_obj)
        if config_obj['all_plots']:
            print("Postprocessing all Plots")
            postprocess_all_plots(config_obj)
        if config_obj['all_tables']:
            print("Postprocessing all Tables")
            postprocess_all_tables(config_obj)
    elif config_obj['dataframes']['vertex_df'] or config_obj['dataframes']['tree_df'] or config_obj['plots']['tree_bias_vs_c0'] or config_obj['plots']['vertex_status_vs_id'] or config_obj['plots']['histograms'] or config_obj['tables']['vertex_table'] or config_obj['tables']['tree_table'] or config_obj['tables']['tree_corr_table'] or config_obj['stats']['BEC_histogram']:
        print("Creating at least one thing.")
        if config_obj['dataframes']['vertex_df']:
            postprocess_vertex_df(config_obj)
        if config_obj['dataframes']['tree_df']:
            postprocess_tree_df(config_obj)
        if config_obj['plots']['tree_bias_vs_c0']:
            if config_obj['has_labels']:
                postprocess_tree_bias_vs_c0(config_obj)
            else:
                print("You can't create a bias vs c0 graph: Your data has no labels.")
        if config_obj['plots']['vertex_status_vs_id']:
            postprocess_vertex_status_vs_id(config_obj)
        if config_obj['plots']['histograms']:
            postprocess_histograms(config_obj)
        if config_obj['tables']['vertex_table']: 
            postprocess_vertex_table(config_obj)
        if config_obj['tables']['tree_table']:
            if config_obj['has_labels']:
                postprocess_tree_table(config_obj)
            else:
                print("You can't create a tree table: Your data has no labels.")
        if config_obj['tables']['tree_corr_table']:
            postprocess_tree_corr_table(config_obj)
        if config_obj['stats']['BEC_histogram']:
            postprocess_BEC_list(config_obj)
  
def submit_postprocess_LEAP_job(config_obj, process_jobID):
    # retrieve (dataset, data_subset_type, matrix_name, component_no) from config_obj
    dataset = config_obj['dataset']
    data_subset_type = config_obj['data_subset_type']
    matrix_name = config_obj['matrix_name']
    component_no = config_obj['component_no']
    # then call a bash script that calls preprocess_general with those parameters
    # subprocess.check_call("preprocess_general.sh %s %s %s %s" % (dataset, data_subset_type, matrix_name, str(component_no)))
    LEAP_output = None # Rz added this 
    if config_obj['parallelism'] == 'spark': # Copied from process not tested yet
      print("Submitting process job on LEAP using Spark")
      LEAP_output = subprocess.run(['postprocess/wrapper_postprocess_general.sh', dataset, data_subset_type, matrix_name, str(component_no), str(process_jobID)], stdout=subprocess.PIPE).stdout.decode('utf-8')
    else:
      print("Submitting process job on LEAP (non-Spark).")
      LEAP_output = subprocess.run(['postprocess/wrapper_postprocess_general.sh', dataset, data_subset_type, matrix_name, str(component_no), str(process_jobID)], stdout=subprocess.PIPE).stdout.decode('utf-8')
    print("submit_postprocess_LEAP_job output: ", LEAP_output)
    job_ID = int(LEAP_output.split()[-1])
    return job_ID

if __name__ == "__main__":
  print("Running postprocess main with args: ", sys.argv)
  dataset = str(sys.argv[1])
  data_subset_type = str(sys.argv[2])
  matrix_name = str(sys.argv[3])
  component_no = int(sys.argv[4])
  process_jobID = int(sys.argv[5])
  config_obj = get_yaml_config_obj_by_key_tuple(dataset, data_subset_type, matrix_name, component_no)
  postprocess_locally(config_obj)

