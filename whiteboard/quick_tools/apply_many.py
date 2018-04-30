import subprocess as sp
import argparse
import os

def args_get():
    parser = argparse.ArgumentParser(description='Applies a function to many files')
    parser.add_argument('--work-dir', required=True, help='The directory to which to apply the files')
    parser.add_argument('-p', '--pattern', default='', help='pattern by which to identify files')

    subparsers = parser.add_subparsers(help='Functions to apply to many files')

    reheader_parser = subparsers.add_parser('reheader', help='Apply a header to a number of vcf files')
    reheader_parser.add_argument('--header', required=True, help='The file to use to reheader.')
    reheader_parser.set_defaults(func=action_reheader)

    remove_header_parser = subparsers.add_parser('remove-header', help='Apply a header to a number of vcf files')
    remove_header_parser.set_defaults(func=action_remove_header)

    sed_parser = subparsers.add_parser('sed', help='Apply a header to a number of vcf files')
    sed_parser.add_argument('--sed-string', required=True, help='The value with which to run sed.')
    sed_parser.set_defaults(func=action_modify_within_file)

    return parser.parse_args()


def action_reheader(args, work_dir, files):
    processes = []
    for i in range(len(files)):
        tmp = os.path.join(work_dir, 'temporary_reheader_file_' + str(i))
        cmd = 'cat {header} {current_file} > {tmp_file} && mv {tmp_file} {current_file}'.format(
            header=args.header,
            current_file=files[i],
            tmp_file=tmp)
        proc = sp.Popen(cmd, shell=True)
        procceses.append(proc)

    for handle in processes:
        handle.wait()

def action_remove_header(args, work_dir, files):
    processes = []
    for i in range(len(files)):
        tmp = os.path.join(work_dir, 'temporary_remove_header_file_' + str(i))
        cmd = "zgrep -v '^#' {current_file} > {tmp_file} && mv {tmp_file} {current_file}".format(
            current_file=files[i],
            tmp_file=tmp)
        proc = sp.Popen(cmd, shell=True)
        processes.append(proc)

    for handle in processes:
        handle.wait()

def action_modify_within_file(args, work_dir, files):
    processes = []
    for i in range(len(files)):
        tmp = os.path.join(work_dir, 'temporary_reheader_file_' + str(i))
        cmd = 'sed {sed_pattern} {current_file} > {tmp_file} && mv {tmp_file} {current_file}'.format(
            sed_pattern=args.sed_string,
            current_file=files[i],
            tmp_file=tmp)
        proc = sp.Popen(cmd, shell=True)
        processes.append(proc)

    for handle in processes:
        handle.wait()


def main():
    args = args_get()
    work_dir = args.work_dir
    files = [os.path.join(work_dir, f) for f in os.listdir(work_dir) if args.pattern in f]
    args.func(args, work_dir, files)

if __name__ == '__main__':
    main()