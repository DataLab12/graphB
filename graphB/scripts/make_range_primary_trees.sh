#!/bin/bash
echo "|++++++++++| Putting in a bunch of sbatch job (high votes):"

declare -a range_votes_options=(36 39 42)

declare -a cluster_options=(0)
declare -a conn_comp_options=(0)
NUM_RANDOM_TREES=100
RECREATE_LOW_HI_AV=0

for range_primary_matrix in "${range_votes_options[@]}"
do
    sbatch sbatch_generic_trees.sh "wiki" "range_primary_cycles" $range_primary_matrix 0 1 $NUM_RANDOM_TREES $RECREATE_LOW_HI_AV 1 "range_primary_cycles $range_primary_matrix $NUM_RANDOM_TREES" &
    echo "|+| Submitted batch job: range_votes $range_primary_matrix"
done
