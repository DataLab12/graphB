import yaml
from sys import argv
import glob
import os

### can be used to make a bunch of subdirectories at once all with their own copy of 0.yaml
### USAGE: python <program name> <0.yaml file to be copied from> <Raw_Data directory to source from> <config directory to put new 0.yaml files into> <first word of raw data files to match on>
### Example: If you have a bunch of new sub data all part of parent dataset 'Apples' and the edges and users files
### look like apples_gala_edges.csv, apples_fuji_edges.csv, apples_red_edges.csv, then you would run the program as follows:
### python create_graphB_configs.py existingYamlDir/0.yaml data-Apples/Raw_Data/ graphB/configs/Apples/apples apples
### The program will iterate through all of the raw data files that start with the word apples and then create directories inside of
### graphB/configs/Apples/apples to match the sub names, in this example you would have three directories: apples/gala/0.yaml,
### apples/fuji/0.yaml, and apples/red/0.yaml. Each respective yaml file with have the config options changed to match the proper dataset
### or subset so graphB will be able to recognize them properly and run them.  

file = argv[1]
raw_file_dir = argv[2]
config_file_dir = os.path.abspath(argv[3])
dataset_matcher = argv[4]

dataset = config_file_dir.split('\\')[-2]

with open(file) as config:
    config_data = yaml.load(config, Loader=yaml.FullLoader)
    print(config_data)
    raw_file_list = glob.glob(os.path.join(raw_file_dir, dataset_matcher + '*.csv'))
    for raw_file in raw_file_list:
        current_sub_name = os.path.basename(raw_file).split('_')[1]
        current_dir_name = os.path.join(config_file_dir, current_sub_name)
        print(current_dir_name)
        try:
            os.makedirs(current_dir_name)
            config_data['dataset'] = dataset
            config_data['data_subset_type'] = dataset_matcher
            config_data['matrix_name'] = current_sub_name
            print(config_data)
            with open(current_dir_name + '\\0.yaml', 'w') as new_yaml:
                output = yaml.dump(config_data, new_yaml)
        except:
            continue
