import subprocess as sp
import time

v81 = '/usr/local/software/vep/ensembl-tools-release-81/scripts/variant_effect_predictor/variant_effect_predictor.pl'
v90 = '/usr/local/software/vep/ensembl-vep-release-90.10/vep'
inf = '/scratch/personal/jmcgonigle/onekgenomes/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz'
out_81 = '/scratch/personal/jmcgonigle/test_pipelines/vep/81.vcf'
out_90 = '/scratch/personal/jmcgonigle/test_pipelines/vep/90.vcf'
out_90_with_90 = '/scratch/personal/jmcgonigle/test_pipelines/vep/90_with_90.vcf'
out_90_with_90_tabixed = '/scratch/personal/jmcgonigle/test_pipelines/vep/90_with_90_tabixed_cache.vcf'
fasta = '/scratch/data/reference/GRCh37/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa'


def timeit(method):
    def timed(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        time_string = "{func_name} took:--- {sec} seconds ---".format(func_name=method.__name__, sec=time.time() - start_time)
        return result, time_string

    return timed

@timeit
def run_vep(vep_script, cache, vep_input, vep_output, fasta, cache_version):
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
    --no_progress \
    --force_overwrite \
    --no_stats \
    --fasta {VEP_FASTA} \
    --merged \
    --all_refseq \
    --assembly {assembly} \
    --cache_version {cache_v}
    '''.format(
        script=vep_script,
        VEP_CACHE=cache,
        output=vep_output,
        input=vep_input,
        VEP_FASTA=fasta,
        assembly='GRCh37',
        cache_v=cache_version
    )
    print(cmd)
    proc = sp.Popen(cmd, shell=True)
    proc.wait()


def main():
    # _, v81_time = run_vep(v81,'/scratch/data/VEP', inf, out_81, fasta, '81')
    # print('running Vep90 with old cache')
    # _, v90_time = run_vep(v90, '/scratch/data/VEP', inf, out_90, fasta, '81')
    # print('Vep 81')
    # print(v81_time)
    # print('Vep 90')
    # print(v90_time)

    _, v90_with_90_time = run_vep(v90, '/scratch/data/VEP_90_GRCH37', inf, out_90_with_90_, fasta, '90')
    print(v90_with_90_time)
if __name__ == '__main__':
    main()
