import pandas as pd
import os


onek = pd.read_csv('/scratch/personal/jmcgonigle/random_work/cache/21.main', sep='\t', header=None)
vep = pd.read_csv('/scratch/personal/jmcgonigle/random_work/cache/VEP.main', sep='\t', header=None)

vep_info = vep['7']
onek_info = onek['5']

def isolate_values(column):
    column.str.split(';')[1][3:]






with open('/scratch/personal/jmcgonigle/random_work/cache/VEP.values', 'r') as f, open('/scratch/personal/jmcgonigle/random_work/cache/VEP.values_fixed', 'w') as o:
    for line in f:
        values = line.strip().split(',')
        if len(values) == 1:
            o.write(values[0] + '\n')
        else:
            o.write(str(max([float(x) for x in values])) + '\n')