import subprocess as sp
import argparse
import os
import time


def args_get():
    parser = argparse.ArgumentParser(description='Applies a function to many files')

    subparsers = parser.add_subparsers(help='Functions to apply to many files')

    bcftools_targets_parser = subparsers.add_parser('bcftools-targets', help='Apply a header to a number of vcf files')
    bcftools_targets_parser.add_argument('--vcf-file', required=True, help='The input vcf file to us in benchmarking.')
    bcftools_targets_parser.add_argument('--bed-file', required=True, help='The bed file to use as targets in benchmarking.')
    bcftools_targets_parser.add_argument('--output-file', required=True, help='The bed file to use as targets in benchmarking.')
    bcftools_targets_parser.set_defaults(func=action_bcftools_targets)

    vep_parser = subparsers.add_parser('VEP', help='Run vep with optional parameters')
    vep_parser.add_argument('--input-vcf', required=True,
                                         help='The path to the input vcf file to us in benchmarking.')
    vep_parser.add_argument('--vep-script', required=True,
                                         help='The path to the script of vep to in benchmarking.')
    vep_parser.add_argument('--vep-cache', required=True,
                                         help='The path to the vep cache to use in benchmarking.')
    vep_parser.add_argument('--vep-cache-version', required=True,
                                         help='The cache version to use in benchmarking.')
    vep_parser.add_argument('--assembly', required=True,
                                         help='The assembly to use in benchmarking.')
    vep_parser.add_argument('--reference-fasta', required=True,
                                         help='The path to the reference fasta to use in benchmarking.')
    vep_parser.add_argument('--output-file', required=True,
                                         help='The path to the output file.')
    vep_parser.add_argument('--no-progress', required=True, type=bool,
                                         help='Silence progress.')
    vep_parser.add_argument('--no-stats', required=True, type=bool,
                                         help='Silence stats.')
    vep_parser.add_argument('--use-given-ref', required=True, type=bool,
                                         help='Stops it using the transcript ref.')
    vep_parser.add_argument('--check-frequency', required=False,  type=float, default = None,
                            help='Stops it using the transcript ref.')
    vep_parser.set_defaults(func=action_vep)


    return parser.parse_args()


def timeit(method):
    def timed(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        time_string = "{func_name} took:--- {sec} seconds ---".format(func_name=method.__name__, sec=time.time() - start_time)
        print(time_string)
        return result, time_string

    return timed

@timeit
def action_bcftools_targets(args):
    cmd = '''bcftools view --targets-file {bed_file} {vcf_file} > {output_file}'''.format(bed_file=args.bed_file,
                                                                                           vcf_file=args.vcf_file,
                                                                                           output_file=args.output_file)
    proc = sp.Popen(cmd, shell=True)
    proc.wait()

@timeit
def action_vep(args):
    cmd = '''
       perl {script} \
       --vcf \
       --hgvs \
       --offline \
       --everything \
       --dir_cache {VEP_CACHE} \
       --input_file {input} \
       --format vcf \
       --output_file {output} \
       --force_overwrite '''.format(
        script = args.vep_script,
        VEP_CACHE=args.vep_cache,
        input=args.input_vcf,
        output=args.output_file)

    if args.no_progress is True:
        cmd += '''--no_progress '''

    if args.no_stats is True:
        cmd+='''--no_stats '''

    if args.use_given_ref is True:
        cmd += '''--use_given_ref '''

    cmd += ''' --fasta {VEP_FASTA} \
       --merged \
       --all_refseq \
       --assembly {assembly} \
       --cache_version {cache_v}
       --fork 4'''.format(
    VEP_FASTA = args.reference_fasta,
    assembly = args.assembly,
    cache_v = args.vep_cache_version)
    print('--------------------')
    print(args.check_frequency)
    print(args.check_frequency is True)
    print(args.check_frequency is False)
    print('--------------------')
    if args.check_frequency is not None:
        cmd+= '''
         --check_frequency \
         --freq_pop 1KG_ALL \
         --freq_freq 0.05 \
         --freq_gt_lt gt \
         --freq_filter exclude'''.format(args.check_frequency)
    else:
        pass

    print(cmd)
    proc = sp.Popen(cmd, shell=True)
    proc.wait()


def main():
    args = args_get()

    _, time_taken = args.func(args)
    print(time_taken)
if __name__ == '__main__':
    main()

