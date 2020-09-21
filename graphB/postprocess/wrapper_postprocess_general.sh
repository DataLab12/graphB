#!/bin/sh

sbatch --dependency=afterany:$5 postprocess/postprocess_general.sh $1 $2 $3 $4 $5