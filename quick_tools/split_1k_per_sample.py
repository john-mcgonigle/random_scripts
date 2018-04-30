import argparse
import os
from datetime import datetime as dt
import subprocess as sp

chrms = list(range(1,23))
chrms += ['X', 'Y']


def args_get():
    parser = argparse.ArgumentParser(description='Applies a function to many files')

    parser.add_argument('--work-dir', required=True, help='The directory containing the merged vcfs.')
    parser.add_argument('--output-dir', required=True, help='An output file to store the patients in.')
    return parser.parse_args()



def create_patient():
    args = args_get()
    file_paths = [os.path.join(args.work_dir, path) for path in os.listdir(args.work_dir) if '.vcf' in path]

    split_processes = []
    chrom_dirs = []
    for chr_no in chrms:
        pattern = 'chr'+str(chr_no)
        print(pattern)
        path = ''.join([f for f in file_paths if pattern + '.' in f])
        current_dir = os.path.join(args.output_dir, pattern)

        if os.path.isdir(current_dir) is not True:
            os.mkdir(current_dir)
        print(current_dir)

        split_processes = split_chr(path, current_dir, split_processes)
        chrom_dirs.append(current_dir)

        if pattern == 'chrX':
            all_indiv = [path for path in os.listdir(current_dir) if '.vcf.gz' in path]

        if pattern == 'chrY':
            males = [path for path in os.listdir(current_dir) if '.vcf.gz' in path]
    #
    # for handle in split_processes:
    #     handle.wait()

    processes = []
    progress = 0
    females = list(set(all_indiv) - set(males))

    for male in males:
        processes, progress = make_individual(chrom_dirs, male, os.path.join(args.output_dir, male), processes, progress)

    print(chrom_dirs)
    del(chrom_dirs[chrom_dirs.index('/scratch/data/oneK/out/supplementary/out/chrY')])

    for female in females:
       processes, progress = make_individual(chrom_dirs, female, os.path.join(args.output_dir, female), processes, progress)


    handle_processes(processes, progress)

def handle_processes(processes, progress):
    print('-------------------- Percentage of samples  ' + str(progress / 2500)
          + ' started at: ' + str(dt.now().isoformat())
          + ' --------------------')

    for handle in processes:
        handle.wait()

    print('-------------------- Percentage of samples  ' + str(progress / 2500)
          + ' finished at: ' + str(dt.now().isoformat())
          + ' --------------------')

def make_individual(chr_dirs, sample, output_path, processes, progress):
    paths = ' '.join(os.path.join(path, sample) for path in chr_dirs)
    cmd =''' bcftools concat {PATHS} | \
    bcftools norm --multiallelics - | \
    bcftools view --min-ac=1 \
    --output-file {OUTPUT_PATH} \
    --output-type 'z' '''.format(PATHS=paths, OUTPUT_PATH=output_path)
    print(cmd)
    proc = sp.Popen(cmd, shell=True)
    processes.append(proc)
    progress += 1

    if len(processes) == 50:
        handle_processes(processes, progress)

        return [], progress

    else:
        return processes, progress

def split_chr(path, output_dir, processes):
    # cmd = '''bcftools +split {PATH} -Oz -o {OUTPUT_DIR} -i'GT="alt"' '''.format(PATH=path, OUTPUT_DIR=output_dir)
    # print(cmd)
    # proc = sp.Popen(cmd, shell =True)
    # # proc.wait()
    # processes.append(proc)
    return processes



if __name__ == '__main__':
    create_patient()


    #
    #
    # print('-------------------- Sample: ' + sample
    #       + ' finished at: ' + str(dt.now().isoformat())
    #       + ' --------------------')


