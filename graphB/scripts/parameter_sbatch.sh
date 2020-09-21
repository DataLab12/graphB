#!/bin/bash
echo "|++++++++++| Putting in a bunch of sbatch jobs:"

TIMES_TO_RUN=1 # Number of times to run this script

declare -a full_adj_types=(# "low_votes",
                           "primary_cycles"
                           "regular_cycles"
                           #"candidate"
                           )
declare -a election_options=(0 1 2 3 4 5 6)
declare -a cluster_options=(0)
declare -a conn_comp_options=(0)
NUM_RANDOM_TREES=50
RECREATE_LOW_HI_AV=0

# start=`date +%s`

for i in {1..$TIMES_TO_RUN}
do
    for full_adj in "${full_adj_types[@]}"
    do
        for election in "${election_options[@]}"
        do
            sbatch sbatch_generic.sh "$full_adj" $election 0 1 $NUM_RANDOM_TREES $RECREATE_LOW_HI_AV "$full_adj $election $NUM_RANDOM_TREES" &
            echo "|+| Submitted batch job: $i $full_adj $election"
            # end_inner=`date +%s`
            # runtime=$((end_inner-start))
            # echo "|+ Inner +| Inner loop execution time: $runtime (election $election with $full_adj and $NUM_RANDOM_TREES random trees)"
        done
        # end_middle=`date +%s`
        # runtime=$((end_middle-start))
        # echo "|+ Middle +| Middle loop execution time: $runtime (all elections with $full_adj)"
    done
    # end_outer=`date +%s`
    # runtime=$((end_outer-start))
    # echo "|+ Outer +| Outer loop $i execution time: $runtime (all full adjs and all elections with $NUM_RANDOM_TREES)"
done
# end=`date +%s`

# echo "|++++++++++| sbatch jobs sent in."
# runtime=$((end-start))
# echo "|+| TOTAL execution time: $runtime"

