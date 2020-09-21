#!/bin/sh

sbatch --dependency=afterany:$5 process/process_general_spark.sh $1 $2 $3 $4 $5