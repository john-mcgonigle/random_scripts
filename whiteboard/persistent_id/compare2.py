import pandas as pd
import csv
import re
import numpy as np
import sys
import os
import subprocess as sp
import argparse
import itertools
import multiprocessing as mp


def process_vcfs(vcf_files, out_vcfs, min_depth):
    rtn_lst =[]


    for vcf, out_vcf in zip(vcf_files, out_vcfs):
        handles1 = []
        handles2 = []

        rtn_lst.append(out_vcf)

        depth_command = ['bcftools', 'view',
                       '--output-type', 'v']
        if min_depth >1:
            depth_command += ['--include', 'DP>' + str(depth)]

        depth_command += [vcf]

        filter_command = ['bcftools', 'query',
                          '-f', r'%CHROM\t%POS\t%REF\t%ALT\t[%GT]\n',
                          '-o', out_vcf]

        depth = sp.Popen(depth_command, stdout=sp.PIPE)
        column_get = sp.Popen(filter_command, stdin = depth.stdout)

        handles1.append(depth)
        handles2.append(column_get)


    for h1,h2 in zip(handles1, handles2):
        h1.wait()
        h2.wait()

    return rtn_lst


def define_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument('script', help = 'A path to the vcf editing shell script.')
    parser.add_argument('vcf_dir', help='A path to the directory with the vcfs to edit.')
    parser.add_argument('out_dir', help= 'A path to the directory in which to store edited vcfs.')
    parser.add_argument('-depth', help='Min depth at which to filter the vcf.', default=0, type = int)
    return parser.parse_args()


#         dx_m['equal'] = dx_m['Hom_x'] == dx_m['Hom_y']
#
#         a = sum_up = dx_m['equal'].sum()
#         b = sum_up = dx_m['equal'].count()
#
#         print(str(ii) + '\t' + str(jj) + '\t' + files[ii] + '\t' + files[jj] + '\t' + str(a/b) + '\t' + str(b))

def pariwise_comparison(x, y, queue):
    df_x = load_and_encode(x)
    df_y = load_and_encode(y)

    df_m = df_x.merge(df_y, on=['Chr','Loc','Ref','Alt'], how='inner')

    queue.put([x.split('/')[-1].replace('.vcf' , ''), y.split('/')[-1].replace('.vcf' , ''),
               (df_m['Hom_x'] == df_m['Hom_y']).sum()/len(df_m), len(df_m)])

def load_and_encode(f_name):
    df = pd.read_csv(f_name, sep='\t', names=['Chr','Loc','Ref','Alt','Hom'])
    df['Hom'] = encode_gt_column(df['Hom'])
    return df

def encode_gt_column(col):
    tmp = col.str.extract(r'(?P<maternal>[0-9]+)[|/](?P<paternal>[0-9]+)', expand=True)
    tmp = tmp.apply(pd.to_numeric, errors='ignore')
    a = tmp['maternal']
    b = tmp['paternal']
    return (a + b + 1)*(a + b) // 2 + b


def run_vcf_comparison(cores = 20):
    procs = []
    queue = mp.Queue()
    proc_count = 0
    completed = 0

    args = define_args()

    vcf_lst = [os.path.join(args.vcf_dir, f) for f in os.listdir(args.vcf_dir) if '.vcf' in f]

    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir)

    mod_vcf = [os.path.join(args.out_dir, f) for f in os.listdir(args.vcf_dir) if '.vcf' in f]
    file_lst = process_vcfs(vcf_lst, mod_vcf, args.depth)


    possible_combin = list(itertools.combinations(range(len(file_lst)), 2))
    with open(os.path.join(args.out_dir, 'vcf_comparison_summary.vcf'), 'w') as out:
        writer = csv.writer(out)
        writer.writerow(['ID1', 'ID2', 'Proportion', 'n'])
        for combination in possible_combin:
            x = file_lst[combination[0]]
            y = file_lst[combination[1]]
            p = mp.Process(target=pariwise_comparison, args=(x, y, queue))
            p.start()
            procs.append(p)

            completed += 1
            proc_count += 1

            if proc_count == cores or completed == len(possible_combin):
                queue, procs, proc_count = queueManager(queue, procs, writer)


def queueManager(queue, procs, writer):
    for proc in procs:
        proc.join()
        item = queue.get()
        writer.writerow(item)
    return mp.Queue(), list(), 1



if __name__ == '__main__':
    run_vcf_comparison()

