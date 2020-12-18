#!/bin/bash -l

#SBATCH --output="slurmout/%A.txt"
#SBATCH --job-name="Process Spark"
#SBATCH --partition=shared
#SBATCH --mem=60GB
#SBATCH --ntasks-per-node=28
#SBATCH --nodes=4
#SBATCH --time=6-23:59:59

# Epinions is known to work at <= 16, slashdot at <= 20
echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running on $SLURM_NPROCS processors."
echo "Current working directory is `pwd`"

. /home/edh63/miniconda/etc/profile.d/conda.sh

echo "Activating Conda VM"
conda activate cam

echo "Loading Various modules"
. /etc/profile.d/modules.sh

# Load Java 1.8 environment
echo "Loading Java 1.8"
module load java/1.8.0_162

export SPARK_HOME=$HOME/spark-2.3.4-bin-hadoop2.7

echo "Executing tree and balancing on Spark."

$SPARK_HOME/bin/spark-submit --conf "spark.executor.extraJavaOptions=-Djava.io.tmpdir=$HOME/tmp/spark-temp/" --conf "spark.driver.extraJavaOptions=-Djava.io.tmpdir=$HOME/tmp/spark-temp/" --conf "spark.local.dir=$HOME/tmp/spark-temp/" --executor-cores 4 --num-executors 27 --executor-memory 17g --driver-memory 17g process_general.py $1 $2 $3 $4 $5 

echo "Program finished with exit code $? at: `date`"
