#!/bin/bash -l

#SBATCH --output="slurmout/%A.txt"
#SBATCH --job-name="Process Regular"
#SBATCH --partition=shared
#SBATCH --mem=60GB
#SBATCH --ntasks-per-node=28
#SBATCH --nodes=4
#SBATCH --time=6-23:59:59

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Current working directory is `pwd`"

. /home/edh63/miniconda/etc/profile.d/conda.sh
conda activate cam

python  process_general.py $1 $2 $3 $4 $5
echo "Program finished with exit code $? at: `date`"
