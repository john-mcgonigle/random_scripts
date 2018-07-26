import subprocess as sp
import os 
import time
import csv
import sys

input_dir = '/staging/tmp_future_neuro/For_Transfer_to_Congenica/'
out_dir = '/staging/tmp_future_neuro/output'
failed_files = os.path.join(out_dir, 'failing_files.csv')
completed_files = os.path.join(out_dir, 'completed_files.csv')
proc_log = os.path.join(out_dir, 'run_log.csv')

def write_to_log(log_path, sample_name, fq1, fq2):
    with open(log_path, 'a') as log:
        writer = csv.writer(log, delimiter='\t')
        writer.writerow([time.ctime(), sample_name, fq1, fq2])


def get_file_info(path):
    rtn_dct = {}
    with open(path, 'r') as in_csv:
        reader = csv.reader(in_csv)
        next(reader)
        for line in reader:
            rtn_dct[line[0]] = {'gender':line[1], 'hpo':line[2].strip('HP:')}

    return rtn_dct


def process_sample(sample_prefix, r1, r2, name, gender):
    output_directory = os.path.join(out_dir, sample_prefix)
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)


    cmd = '''
    dragen -f -r /staging/human/reference/GRCh37 -1 {R1} \
    -2 {R2} \
    --generate-md-tags true --enable-duplicate-marking true \
    --enable-variant-caller true --enable-map-align-output true \
    --vc-reference /staging/human/reference/hg19/GRCh37.fa \
    --output-directory {OUT_DIR} --vc-sample-name {SAMPLE_NAME} --enable-bam-indexing true \
    --RGSM {SAMPLE_NAME} --RGID {SAMPLE_NAME} --RGPL ILLUMINA \
    --output-file-prefix {SAMPLE_NAME} --vc-sex={GENDER}
    '''.format(R1=r1, R2=r2, OUT_DIR=output_directory, SAMPLE_NAME=name, GENDER=gender)

    proc = sp.Popen(cmd, shell=True, stderr=sp.STDOUT, stdout=sp.PIPE)
    stdout, stderr = proc.communicate()
    
    if proc.returncode != 0:
        print('Sample name ' + name + ' failed.')
        print(cmd)
        print(stderr)
        print(stdout)
        write_to_log(failed_files, name, r1, r2)
        return False
    else:
        write_to_log(completed_files, name, r1, r2)
        return True

def run_log_entry(file_prefix, status):
    with open(proc_log, 'a') as run_log:
        if status is None:
            run_log.write('{X} started processing at {TIME} \n'.format(X=file_prefix, TIME=time.ctime()))
        elif status:
            run_log.write('{X} successfully completed processing at {TIME} \n'.format(X=file_prefix, TIME=time.ctime()))
        else:
            run_log.write('{X} failed at {TIME} \n'.format(X=file_prefix, TIME=time.ctime()))



def main():
    info_dct = get_file_info(os.path.join(input_dir, 'project_733_ir_initial91.csv'))
    fq_1 = [filename for filename in sorted(os.listdir(input_dir)) if 'fastq.gz' in filename and 'R1' in filename]
    fq_2 = [filename for filename in sorted(os.listdir(input_dir)) if 'fastq.gz' in filename and 'R2' in filename]

    file_pairs = [(a,b) for a,b in zip(fq_1, fq_2)]

    for pair in file_pairs:
        r1, r2 = pair
        file_prefix = r1.split('_R')[0]
        sample = r1.split('_')[0]

        if '-rpt' in sample:
            sample = sample.strip('-rpt')

        run_log_entry(file_prefix, None)

        if process_sample(file_prefix, os.path.join(r1), os.path.join(r2), sample, info_dct[sample]['gender']):
            run_log_entry(file_prefix, True)

        else:
            run_log_entry(file_prefix, False)

if __name__ == '__main__':
    main()













