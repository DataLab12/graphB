#!/bin/bash -l

#SBATCH --job-name=$9
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

# setup modules
. /etc/profile.d/modules.sh

# Load Java 1.8 environment
module load java/1.8.0_162

export SPARK_HOME=$HOME/spark-2.3.1-bin-hadoop2.7
# export SPARK_HOME=$HOME/miniconda3/pkgs/pyspark-2.3.1-py37_1

$SPARK_HOME/bin/spark-submit tree_creation/create_trees_general.py $1 $2 $3 $4 $5 $6 $7 $8
# create_trees.py <dataset> <data type> <full adj option (which one)> <cluster?> <split by conn comp?> <num random sts> <recreate low, hi, av trees> <spark?>

echo "Program finished with exit code $? at: `date`"
# $SPARK_HOME/bin/spark-submit tree_creation/create_trees_general.py wiki candidate 3 0 1 1 0
