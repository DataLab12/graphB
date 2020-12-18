#!/bin/bash

IFS=' '

### command line arguments, come from yaml config parameters
dataset=$1
data_subset_type=$2
matrix_name=$3
num_trees=$4
tree_type=$5
parallelism=$6

pre_jobid=$(grep -w 'preprocess_jobID' ../data-${dataset}/Logfiles/${data_subset_type}_${matrix_name}/${num_trees}${tree_type}_${parallelism}_LEAP_logs.txt)
pro_jobid=$(grep -w 'process_jobID' ../data-${dataset}/Logfiles/${data_subset_type}_${matrix_name}/${num_trees}${tree_type}_${parallelism}_LEAP_logs.txt)
post_jobid=$(grep -w 'postprocess_jobID' ../data-${dataset}/Logfiles/${data_subset_type}_${matrix_name}/${num_trees}${tree_type}_${parallelism}_LEAP_logs.txt)

read -a pre_jobid <<< $pre_jobid
read -a pro_jobid <<< $pro_jobid
read -a post_jobid <<< $post_jobid

pre_jobid=${pre_jobid[-1]}
pro_jobid=${pro_jobid[-1]}
post_jobid=${post_jobid[-1]}

cat slurmout/${pre_jobid}.txt slurmout/${pro_jobid}.txt slurmout/${post_jobid}.txt > ../data-${dataset}/Logfiles/${data_subset_type}_${matrix_name}/${num_trees}${tree_type}_${parallelism}_LEAP_output.txt

python make_timing_dfs.py ../data-${dataset}/Logfiles/${data_subset_type}_${matrix_name}/${num_trees}${tree_type}_${parallelism}_LEAP_output.txt
