#!/bin/sh

#SBATCH --partition=short-serial 
#SBATCH -o /gws/nopw/j04/odanceo/dkumar/Q0/PRODUCTION/%j.out 
#SBATCH -e /gws/nopw/j04/odanceo/dkumar/Q0/PRODUCTION/%j.err
#SBATCH --nodes=8
#SBATCH --time=23:59:00
#SBATCH --mem-per-cpu=150000MB



# executable 
#module load jaspy
/apps/jasmin/jaspy/miniconda_envs/jaspy3.8/m3-4.9.2/envs/jaspy3.8-m3-4.9.2-r20211105/bin/python /gws/nopw/j04/odanceo/dkumar/Q0/PRODUCTION/Q0_production.py
/apps/jasmin/jaspy/miniconda_envs/jaspy3.8/m3-4.9.2/envs/jaspy3.8-m3-4.9.2-r20211105/bin/python /gws/nopw/j04/odanceo/dkumar/Q0/PRODUCTION/split_production.py
sh /gws/nopw/j04/odanceo/dkumar/Q0/PRODUCTION/filelists.sh
/apps/jasmin/jaspy/miniconda_envs/jaspy3.8/m3-4.9.2/envs/jaspy3.8-m3-4.9.2-r20211105/bin/python /gws/nopw/j04/odanceo/dkumar/Q0/PRODUCTION/imagedump.py 

