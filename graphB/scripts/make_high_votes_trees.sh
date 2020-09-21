#!/bin/bash
echo "|++++++++++| Putting in a bunch of sbatch job (high votes):"

declare -a high_votes_options=(7) # 0 - 7
# 0 --> more_than_10.h5
# 1 --> more_than_10_voted_voted_for.h5
# 2 --> more_than_20.h5
# 3 --> more_than_20_voted_voted_for.h5
# 4 --> more_than_5.h5
# 5 --> more_than_50.h5
# 6 --> more_than_50_voted_voted_for.h5
# 7 --> more_than_5_voted_voted_for.h5
declare -a cluster_options=(0)
declare -a conn_comp_options=(0)
NUM_RANDOM_TREES=100
RECREATE_LOW_HI_AV=0

for high_votes_matrix in "${high_votes_options[@]}"
do
    sbatch sbatch_generic_trees.sh "wiki" "high_votes" $high_votes_matrix 0 1 $NUM_RANDOM_TREES $RECREATE_LOW_HI_AV 1 "high_votes $high_votes_matrix $NUM_RANDOM_TREES" &
    echo "|+| Submitted batch job: high_votes $high_votes_matrix"
done
