#!/bin/bash
echo "|++++++++++| Putting in a bunch of sbatch job (low votes):"

declare -a low_votes_options=(1) # 0 - 3 (0:100, 1:200, 2:30, 3:50) 
declare -a cluster_options=(0)
declare -a conn_comp_options=(0)
NUM_RANDOM_TREES=54
RECREATE_LOW_HI_AV=0

for low_votes_matrix in "${low_votes_options[@]}"
do
    sbatch sbatch_generic_trees.sh "wiki" "low_votes" $low_votes_matrix 0 1 $NUM_RANDOM_TREES $RECREATE_LOW_HI_AV 1 "low_votes $low_votes_matrix $NUM_RANDOM_TREES" &
    echo "|+| Submitted batch job: low_votes $low_votes_matrix"
done
