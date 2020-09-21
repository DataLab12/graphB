#!/bin/bash
echo "|++++++++++| Putting in a bunch of sbatch jobs (elections):"

declare -a full_adj_types=(# "low_votes",
                           "primary_cycles"
                           #"regular_cycles"
                           #"candidate"
                           )
declare -a election_options=(3) # 0 - 6 
declare -a cluster_options=(0)
declare -a conn_comp_options=(0)
NUM_RANDOM_TREES=200
RECREATE_LOW_HI_AV=0

for full_adj in "${full_adj_types[@]}"
    do
        for election in "${election_options[@]}"
        do
            sbatch sbatch_generic_trees.sh "wiki" "$full_adj" $election 0 1 $NUM_RANDOM_TREES $RECREATE_LOW_HI_AV 1 "$full_adj $election $NUM_RANDOM_TREES" &
            echo "|+| Submitted batch job: $i $full_adj $election"
        done
    done
echo "|++++++++++| sbatch jobs sent in."
