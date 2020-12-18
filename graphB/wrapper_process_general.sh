#!/bin/sh

sbatch --dependency=afterany:$5 process_general.sh $1 $2 $3 $4 $5
