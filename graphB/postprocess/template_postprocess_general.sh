#!/bin/bash -l

#SBATCH --output="slurmout/%A.txt"
#SBATCH --job-name="Postprocess"
#SBATCH --partition=shared
#SBATCH -n 28
#SBATCH --time=23:59:59

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Current working directory is `pwd`"

. /home/jlm346/miniconda3/etc/profile.d/conda.sh
conda activate cam

python postprocess/postprocess_general.py $1 $2 $3 $4 $5
echo "Done"
