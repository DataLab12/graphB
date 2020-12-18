import yaml
from sys import argv
import glob
import os

### can be used to make a bunch of subdirectories at once all with their own copy of the base yaml
### NOTE: The output of this script is not nicely formatted, user would want to follow up by running
###       change_yaml.py after this with a properly formatted yaml as input.
### USAGE: python <program name> <yaml file to be copied from> <Input_Data directory to source from> <config directory to put new yaml files into> <name of data subset>
### Example:
### If you have a bunch of new subset data all part of parent dataset 'Apples'  with data_subset 'apples' and the edges and users files
### look like apples_gala_edges.csv, apples_fuji_edges.csv, apples_red_edges.csv, then you would run the program as follows:
### python create_graphB_configs.py Apples_original_copy.yaml data-Apples/Input_Data/ apples
### The yaml file to be copied from can be any existing yaml file, as this script will copy in the right dataset info to the new yaml.
### Each respective yaml file with have the config options and naming changed to match the proper dataset
### or subset so graphB will be able to recognize them properly and run them.

copy_from_config = argv[1]
input_file_dir = argv[2]
dataset_matcher = argv[3]
config_file_dir = os.getcwd() + os.sep + 'configs' + os.sep

dataset = os.path.dirname(input_file_dir).split(os.sep)[-1].split('-')[1]

with open(copy_from_config) as config:
    config_data = yaml.load(config, Loader=yaml.FullLoader)
    print(config_data)
    input_file_list = glob.glob(os.path.join(input_file_dir, dataset_matcher + '*.csv'))
    for input_file in input_file_list:
        current_sub_name = os.path.basename(input_file).split('_')[1]
        new_yaml_filename = dataset + '_' + dataset_matcher + '_' + current_sub_name + '.yaml'
        print(new_yaml_filename)
        try:
            config_data['dataset'] = dataset
            config_data['data_subset_type'] = dataset_matcher
            config_data['matrix_name'] = current_sub_name
            print(config_data)
            print(config_file_dir + new_yaml_filename)
            with open(config_file_dir + new_yaml_filename, 'w') as new_yaml:
                output = yaml.dump(config_data, new_yaml)
        except:
            continue
