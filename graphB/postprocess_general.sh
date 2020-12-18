#!/bin/bash -l

#SBATCH --output="slurmout/%A.txt"
#SBATCH --job-name="Postprocess"
#SBATCH --partition=shared
#SBATCH -n 28
#SBATCH --time=96:00:00

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Current working directory is `pwd`"

. /home/edh63/miniconda/etc/profile.d/conda.sh
conda activate cam

python postprocess_general.py $1 $2 $3 $4 $5
bash timing_results.sh $1 $2 $3 $6 $7 $8
echo "Done"
