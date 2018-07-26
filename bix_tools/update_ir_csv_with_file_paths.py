import subprocess as sp
import argparse
import os 
import time
import csv
import sys
from collections import defaultdict

# :TODO need to put a reset in if the script fails

def make_ir_csv(path, outpath, file_dct):
    with open(path, 'r') as in_csv, open(outpath, 'w') as out_csv:
        reader = csv.reader(in_csv)
        writer = csv.writer(out_csv)

        header = next(reader)

        writer.writerow(header)

        snv_idx = header.index('vcf_snv')
        bam_idx = header.index('bam')

        for line in reader:
            if line[0] in file_dct:
                line[snv_idx] = file_dct[line[0]]
                writer.writerow(line)
            else:
                print(line[0] + '.vcf is not a file recognised as being in the output directory folders')


def get_sample_dct(samples_dir):
    samples_dct = defaultdict(dict)
    path = os.path.abspath(samples_dir)

    samples = [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]

    for sample in samples: 
        samples_dct[sample] = {'vcf': os.path.join(path, sample, sample + '.hard-filtered.vcf'),
                                'bam': os.path.join(path, sample, sample + '.bam')}

    return samples_dct



def file_setup(path):
    newpath = path+'.old'

    proc = sp.Popen('cp {PATH} {NEWPATH}'.format(PATH=path, NEWPATH=newpath), shell=True, stderr=sp.STDOUT, stdout=sp.PIPE)
    
    stdout, stderr = proc.communicate()
    
    if proc.returncode != 0:
        print('Failure to copy file exiting to avoid rewrite')
        sys.exit(1) 

    return newpath 

        
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ir-csv', required=True)
    parser.add_argument('-wd', '--work-dir', required=True)
    args = parser.parse_args()

    ir_path = args.ir_csv

    original_file = file_setup(ir_path)
  

    file_dct = get_sample_dct(args.work_dir)

    make_ir_csv(original_file, ir_path, file_dct)



if __name__ == '__main__':
    main()


