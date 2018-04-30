import subprocess as subprocess
import os
import argparse as ap
import csv

def define_args():
    parser = ap.ArgumentParser(description='A script to count all the variants of all the vcfs in a directory.')
    parser.add_argument('--dir', required=True,
                        help='The path to a the directory in question e.g./fake/path/to/fake_dir/')
    parser.add_argument('--out', required=True,
                        help='The path to a the directory in question e.g./fake/path/to/fake_dir/')
    return parser.parse_args()


def get_variant_count():
    args = define_args()
    with open(args.out, 'w') as o:
        writer = csv.writer(o, delimiter='\t')
        writer.writerow(['File_path', 'Value'])
        total = int()
        file_paths = [f for f in os.listdir(args.dir) if '.vcf' in f ]

        processes = []
        
        for filepath in file_paths:
            if filepath[-3:] == '.gz':
                cmd = "zgrep -v '#' "+ os.path.join(args.dir, filepath) + " | wc"
            else:
                cmd = "grep -v '#' "+ os.path.join(args.dir, filepath) + " | wc"

            print(cmd)
            handle = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            processes.append((filepath, handle))

        for pair in processes:
            path, handle = pair
            handle.wait()
            line = str(next(handle.stdout))
            value = [int(x) for x in line.split(' ') if x != ''][0]

            total += value
            writer.writerow([path, value])
        writer.writerow(['Total', total])


if __name__ == '__main__':
    get_variant_count()

