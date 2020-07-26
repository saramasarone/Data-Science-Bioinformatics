#!/bin/sh
#$ -cwd           # Set the working directory for the job to the current directory
#$ -pe smp 1      # Request cores
#$ -l h_rt=12:0:0  # Request hour runtime
#$ -l h_vmem=32G   # Request GB RAM
#$ -t 3-50

module load anaconda3
conda activate kallisto_env


./kallisto_bash_array.sh ${SGE_TASK_ID}
