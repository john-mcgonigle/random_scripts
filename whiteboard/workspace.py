import pysam
import pandas as pd
import subprocess as sp
import time

columns = ['chrom', 'pos', 'ref', 'alt', 'sample_1_gt', 'sample_1_dp', 'sample_1_ad',
 'sample_2_gt', 'sample_2_dp', 'sample_2_ad', 'sample_3_gt', 'sample_3_dp', 'sample_3_ad']

def load_variant_file(filepath):
    return pysam.VariantFile(filepath)


def get_variant_information(line):
    info = [line.chrom, line.pos, line.ref, line.alts]
    sample_info = get_sample_info(line)
    return info + sample_info


def get_sample_info(line):
    rtn_lst = []
    for sample in line.samples:
        GT = tuple(sorted(line.samples[sample]['GT']))
        DP = line.samples[sample]['DP']
        AD = line.samples[sample]['AD']
        rtn_lst.extend([GT,DP,AD])
    return rtn_lst

def main(filepath):
    start = time.time()
    vcf = load_variant_file(filepath)
    rtn_lst = []
    for line in vcf:
        rtn_lst.append(get_variant_information(line))

    print(rtn_lst[0])
    df = pd.DataFrame(rtn_lst, columns=columns)

    print(df.head(n=10))
    print(time.time()-start)

main('/Users/john.mcgonigle/ngps/EGA/vcfs/processed_vcfs/formatted_merged_family.vcf.gz')