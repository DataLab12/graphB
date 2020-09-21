#!/bin/bash
echo "|++++++++++| Putting in a bunch of sbatch jobs:"

declare -a candidate_options=(0 1 2 3 4 5) # 0 - 6
declare -a cluster_options=(0)
declare -a conn_comp_options=(0)
NUM_RANDOM_TREES=54
RECREATE_LOW_HI_AV=0

for candidate_matrix in "${candidate_options[@]}"
do  
   sbatch sbatch_generic_trees.sh "wiki" "candidate" $candidate_matrix 0 1 $NUM_RANDOM_TREES $RECREATE_LOW_HI_AV 1 "candidate $candidate_matrix $NUM_RANDOM_TREES" &
   echo "|+| Submitted batch job: candidate $candidate_matrix"
done

echo "|++++++++++| sbatch jobs sent in."
