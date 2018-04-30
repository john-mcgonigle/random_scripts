import subprocess as sp
import os
import argparse as ap
import csv
import numpy as np


def define_args():
    parser = ap.ArgumentParser(description='A script break files into even pieces of other files.')
    parser.add_argument('--dir', required=True,
                        help='The path to a the directory containing the vcfs e.g./fake/path/to/fake_dir/')
    parser.add_argument('--variant-counts', required=True,
                        help='The path to a file containing the no. of variants in each chromosome')
    parser.add_argument('--out-dir', required=True,
                        help='The path to the directory to output the ten patients into e.g./fake/path/to/fake_dir/')
    parser.add_argument('--parts', required=True, type=int,
                        help='Number to subset files into')
    return parser.parse_args()


def intersect_file(i, j, filepath, outfile):
    cmd = "zgrep -v '#' {path} | cut -f1,2,3,4,5,6,7,8,9,10 |  awk 'NR >= {start_index} && NR <= {end_index}' ".format(
        path=filepath,
        start_index=i,
        end_index=j)
    # print(cmd)
    proc = sp.Popen(cmd, shell = True, stdout=outfile)

    return proc

#
# def create_tmp_files(dir_path, file_paths, bin_dct):
#     processes = []
#     processing_dct = {}
#
#     for i in range(len(file_paths)):q
#         tmp = os.path.join(dir_path, 'tmp' + str(i))
#         file_path = os.path.join(dir_path, file_paths[i])
#
#         if file_path[-3:] == '.gz':
#             cmd = "zgrep -v '#' "
#         else:
#             cmd = "grep -v '#' "
#
#         cmd += file_path + ' > ' + tmp
#         # print(cmd)
#         proc = sp.Popen(cmd, shell=True)
#
#         processes.append(proc)
#         processing_dct[os.path.basename(file_path)] = (tmp, bin_dct[os.path.basename(file_path)])
#
#     return processing_dct, processes


def generate_bins(variant_file, n):
    file_dct = {}
    with open(variant_file) as inf:
        reader = csv.reader(inf, delimiter ='\t')
        next(reader) # Skip header
        for line in reader:
            path, file_variant_count = line
            if path != 'Total':
                start = range(1, int(file_variant_count), int(round(int(file_variant_count) / n)))
                end = [x - 1 for x in start[1:]]
                end.append(file_variant_count)

                file_dct[path] = [(x,y) for x,y in zip(start, end)]

    return file_dct

def make_n_files():
    args = define_args()
    header = '\t'.join(['#CHROM', 'ID', 'POS', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO' ])
    n = args.parts
    file_bin_dct = generate_bins(args.variant_counts, n)

    # processing_dct, processes = create_tmp_files(args.dir, file_bin_dct.keys(), file_bin_dct)
    #
    # for proc in processes:
    #     proc.wait()

    file_dct = {}
    for i in range(n):
        current = open(os.path.join(args.out_dir, 'patient_' + str(i) + '.vcf'), 'a')
        current.write(header)
        file_dct[str(i)] = current

    for chrom, bins in file_bin_dct.items():
        file_path = os.path.join(args.dir, chrom)

        processes = []
        for i in range(n):

            start, end = bins[i]
            processes.append(intersect_file(start, end, file_path, file_dct[str(i)]))

        for handle in processes:
            handle.wait()

    for i in range(n):
        file_dct[str(i)].close()


if __name__ == '__main__':
    make_n_files()












            
        