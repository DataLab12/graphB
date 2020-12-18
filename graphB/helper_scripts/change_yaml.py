import os
import sys
import yaml

### MEANT TO BE USED IF USER STILL HAS OLD YAML CONFIG FILE FORMAT (pre-November 2020)
### This script will reformat all yaml files in the graphB directory to be
### uniform layout and have the most recent config options in them.
### It will copy line for line the copy_file argument over the old yaml files with
### their old info intact.
### NOTE: This script is super flimsy and easily breakable. Made for a very specific use
###       case and changing the output of the script will involve changing some
###       hardcoded stuff.

### USAGE: *** RUN from graphB directory ***
### example run: python ./helper_scripts/change_yaml.py <path to properly formatted file>


copy_file = sys.argv[1]
yaml_contents_list = []
copy_file = os.path.relpath(copy_file)
dataset_keys = ['dataset', 'data_subset_type', 'matrix_name']

def format_value(yaml_value):
    if isinstance(yaml_value, bool):
        if yaml_value:
            return 'Yes'
        else:
            return 'No'
    elif isinstance(yaml_value, int):
        return str(yaml_value)
    else:
        return yaml_value

for root, dirs, files in os.walk('.', topdown = True):
    for name in files:
        if name.split('.')[-1] == 'yaml':
            if os.path.relpath(os.path.join(root,name)) != copy_file:
                with open(os.path.join(root,name), 'r') as current_file:
                   file_contents = yaml.load(current_file, Loader=yaml.FullLoader)
                   if file_contents not in yaml_contents_list:
                       yaml_contents_list.append(file_contents)

with open(copy_file, 'r') as copy_file:
    for old_yaml in yaml_contents_list:
        name_params = [old_yaml['dataset'], old_yaml['data_subset_type'], old_yaml['matrix_name']]
        for item in name_params:
            item_index = name_params.index(item)
            word_list = item.split('_')
            if len(word_list) > 1:
                for word in word_list:
                    index = word_list.index(word)
                    if index != 0:
                        word_separated = list(word)
                        word_separated[0] = word_separated[0].upper()
                        word_list[index] = "".join(word_separated)
                name_params[item_index] = ''.join(word_list)
        new_filename = 'configs/' + name_params[0] + '_' + name_params[1] + '_' + name_params[2] + '.yaml'
        with open(new_filename, 'w') as new_yaml:
            for line in copy_file.readlines():
                if line.startswith('#') or line.startswith('\n'):
                    new_yaml.write(line)
                elif line.split(':')[0] in old_yaml.keys():
                    yaml_key = line.split(':')[0]
                    key_comment = line.split('#')[-1]
                    if not isinstance(old_yaml[yaml_key], dict) and yaml_key not in dataset_keys:
                        value = old_yaml[yaml_key]
                        line_to_write = yaml_key + ': ' + format_value(value) + ' # ' + key_comment
                        new_yaml.write(line_to_write)
                    elif yaml_key in dataset_keys:
                        index = dataset_keys.index(yaml_key)
                        value = name_params[index]
                        line_to_write = yaml_key + ': ' + format_value(value) + ' # ' + key_comment
                        new_yaml.write(line_to_write)
                    elif yaml_key == 'tree_type':
                        try:
                            line_to_write = yaml_key + ': # ' + key_comment + '  random: ' + format_value(old_yaml[yaml_key]['random_MST']) + '\n  breadth: ' + format_value(old_yaml[yaml_key]['breadth']) + '\n  depth: ' + format_value(old_yaml[yaml_key]['depth']) + '\n'
                        except KeyError:
                            line_to_write = yaml_key + ': # ' + key_comment + '  random: ' + format_value(old_yaml[yaml_key]['random']) + '\n  breadth: ' + format_value(old_yaml[yaml_key]['breadth']) + '\n  depth: ' + format_value(old_yaml[yaml_key]['depth']) + '\n'
                        new_yaml.write(line_to_write)
                    elif yaml_key == 'dataframes':
                        line_to_write = yaml_key + ':\n  vertex_df: ' + format_value(old_yaml[yaml_key]['vertex_df']) + ' # Need to make this to generate status\n'
                        new_yaml.write(line_to_write)
                    elif yaml_key == 'plots':
                        line_to_write = yaml_key + ':\n  tree_bias_vs_c0: ' + format_value(old_yaml[yaml_key]['tree_bias_vs_c0']) + ' # This option works if the dataset has outcomes.\n  vertex_status_vs_id: ' + format_value(old_yaml[yaml_key]['vertex_status_vs_id']) + ' # This option is what outputs the status vs. id csvs and pngs'
                        new_yaml.write(line_to_write)
                elif line.split(':')[0] == 'preprocess':
                    key_comment = line.split('#')[-1]
                    line_to_write = 'preprocess: ' + format_value(old_yaml['preprocess_again']) + ' # ' + key_comment
                    new_yaml.write(line_to_write)
                elif line.split(':')[0] == 'num_trees':
                    key_comment = line.split('#')[-1]
                    line_to_write = 'num_trees: ' + format_value(old_yaml['num_random_trees']) + ' # ' + key_comment
                    new_yaml.write(line_to_write)
                elif line.split(':')[0] == 'postprocess':
                    key_comment = line.split('#')[-1]
                    line_to_write = 'postprocess: ' + format_value(old_yaml['postprocess_again']) + ' # ' + key_comment
                    new_yaml.write(line_to_write)
        print("wrote yaml: ", new_yaml)
        copy_file.seek(0)
