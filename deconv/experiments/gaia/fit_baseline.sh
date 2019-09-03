#!/bin/sh
#SBATCH -N 1      # nodes requested
#SBATCH -n 1      # tasks requested
#SBATCH --mem=8000  # memory in Mb
#SBATCH --cpus-per-task=8
#SBATCH --time=0-10:00:00
#SBATCH -o output/baseline-%A_%a.txt  # send stdout to outfile
#SBATCH -e output/baseline_error-%A_%a.txt  # send stderr to errfile
#SBATCH --partition=apollo

source ~/.bashrc
conda activate deconv

export PYTHONPATH=${PYTHONPATH}:${HOME}/original_xd/py/

python deconv/experiments/gaia/fit_gaia_baseline.py -c 256 -e 20 -w=0.001 -k 10 data/gaia_sample_mag.npz results/baseline_256_${SLURM_JOBID}
