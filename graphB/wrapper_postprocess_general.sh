#!/bin/sh

sbatch --dependency=afterany:$5 postprocess_general.sh $1 $2 $3 $4 $5 $6 $7 $8 
