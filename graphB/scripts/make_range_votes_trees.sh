#!/bin/bash
echo "|++++++++++| Putting in a bunch of sbatch job (high votes):"

declare -a range_votes_options=(30) #(0 1 2 3 4 5 6 7 8)
# 0 --> above_40_vvf.h5
# 1 --> above_50.h5
# 2 --> from_10_to_30.h5
# 3 --> from_1_to_20.h5
# 4 --> from_1_to_20_vvf.h5
# 5 --> from_20_to_40.h5
# 6 --> from_20_to_40_vvf.h5
# 7 --> from_30_to_50.h5
# 8 --> from_40_to_60.h5
declare -a cluster_options=(0)
declare -a conn_comp_options=(0)
NUM_RANDOM_TREES=54
RECREATE_LOW_HI_AV=0

for range_votes_matrix in "${range_votes_options[@]}"
do
    sbatch sbatch_generic_trees.sh "wiki" "range_votes" $range_votes_matrix 0 1 $NUM_RANDOM_TREES $RECREATE_LOW_HI_AV 1 "range_votes $range_votes_matrix $NUM_RANDOM_TREES" &
    echo "|+| Submitted batch job: range_votes $range_votes_matrix"
done
