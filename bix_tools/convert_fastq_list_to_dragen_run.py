import argparse
import csv
import subprocess as sp
import os
import time
import sys

from collections import defaultdict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--ir-csv', required=True)
    parser.add_argument('-fq', '--fq-csv', required=True)
    parser.add_argument('-o', '--out-dir', required=True)
    args = parser.parse_args()

    failed_files = os.path.join(args.out_dir, 'failed_files.txt')
    processed_files = os.path.join(args.out_dir, 'processed_files.txt')
    proc_log = os.path.join(args.out_dir, 'run_log.csv')

    sample_dct = get_info_dct(args.ir_csv, get_sample_info)
    run_info_dct, fastq_csv_header = get_info_dct(args.fq_csv, get_run_info)

    with open(proc_log, 'a') as run_log:

        # print(run_info_dct)

        for sample in sample_dct:

            sample_run_dct = run_info_dct[sample]

            fastq_csv_path = os.path.join(os.path.dirname(args.fq_csv), sample + '.csv')
            make_fastq_csv(fastq_csv_path, fastq_csv_header, sample_run_dct)

            sample_directory = os.path.join(args.out_dir, sample)

            if not os.path.isdir(sample_directory):
                os.mkdir(sample_directory)

            run_log_entry(run_log, sample, None)

            if submit_dragen(sample, sample_dct[sample], sample_directory, (failed_files, processed_files), fastq_csv_path):
                run_log_entry(run_log, sample, True)

            else:
                run_log_entry(run_log, sample, False)



def get_info_dct(path, processing_func):
    with open(path, 'r') as inf:
        reader = csv.reader(inf)

        return processing_func(reader)


def get_run_info(reader):
    header =next(reader)

    sample_dct = defaultdict(dict)

    for line in reader:
        if line[1] not in sample_dct:
             sample_dct[line[1]] = defaultdict(dict)

        lane_read = os.path.basename(line[4])
        sample_dct[line[1]][lane_read] = {  'RGSM':line[1],
                                            'RGID':line[0],
                                            'Library':line[2],
                                            'RGPL':'Illumina',
                                            'SampleID': line[1],
                                            'Lane':line[3], 
                                            'Read1':line[4], 
                                            'Read2':line[5]}

    return sample_dct, header

def make_fastq_csv(path, header, sample_run_dct):
    with open(path, 'w') as outf:
        writer = csv.DictWriter(outf, fieldnames=['SampleID', 'RGID', 'RGSM', 'Library', 'RGPL', 'Lane', 'Read1', 'Read2'])

        for sample in sample_run_dct:
            writer.writeheader()
            writer.writerow(sample_run_dct[sample])



def get_sample_info(reader):
    sample_dct = defaultdict(str)
    next(reader)

    for line in reader:
        sample_dct[line[0]] = line[1]
    return sample_dct



def write_to_log(log_path, sample_name, gender, csv_path):
    with open(log_path, 'a') as log:
        writer = csv.writer(log, delimiter='\t')
        writer.writerow([, sample_name, gender, csv_path])


def run_log_entry(run_log, file_prefix, status):
        if status is None:
            run_log.write('{X} started processing at {TIME} \n'.format(X=file_prefix, TIME=time.ctime()))
        elif status:
            run_log.write('{X} successfully completed processing at {TIME} \n'.format(X=file_prefix, TIME=time.ctime()))
        else:
            run_log.write('{X} failed at {TIME} \n'.format(X=file_prefix, TIME=time.ctime()))


def submit_dragen(sample, gender, outdir, log_paths, fq_csv_path):
    failed_files, processed_files = log_paths

    if gender == 'Unknown':
        gender = None

    cmd = '''
    dragen -f -r /staging/human/reference/GRCh37 \
    --fastq-list {FQ_CSV} \
    --generate-md-tags true --enable-duplicate-marking true \
    --enable-variant-caller true --enable-map-align-output true \
    --vc-reference /staging/human/reference/hg19/GRCh37.fa \
    --output-directory {OUT_DIR} --vc-sample-name {SAMPLE_NAME} --enable-bam-indexing true \
    --output-file-prefix {SAMPLE_NAME} --vc-sex={GENDER}
    '''.format(FQ_CSV=fq_csv_path,
                OUT_DIR=outdir, 
                SAMPLE_NAME=sample,
                GENDER=gender)


    proc = sp.Popen(cmd, shell=True, stderr=sp.STDOUT, stdout=sp.PIPE)
    stdout, stderr = proc.communicate()
    
    if proc.returncode != 0:
        print('Sample name ' + sample + ' failed.')
        print(cmd)
        print(stderr)
        print(stdout)
        write_to_log(failed_files, sample, gender, fq_csv_path)
        return False
    else:
        write_to_log(processed_files, sample, gender, fq_csv_path)
        return True


if __name__ == '__main__':
    main()
