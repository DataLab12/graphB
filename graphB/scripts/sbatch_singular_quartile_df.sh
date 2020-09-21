#!/bin/bash -l

#SBATCH --job-name="Quartile DFs"
#SBATCH --partition=shared
#SBATCH -n 28
#SBATCH --time=6-23:59:59
#SBATCH --mail-user=jlm346@txstate.edu
#SBATCH --mail-type=end

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Current working directory is `pwd`"

python analysis/create_stats.py $1 
echo "Done"