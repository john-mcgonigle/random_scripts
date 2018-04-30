import argparse
import csv
import os
import subprocess as sp

def get_args():
    parser = argparse.ArgumentParser(description='''A conversion too between various bix file formats''')
    parser.add_argument('--input', required=True, help ='File to convert')
    parser.add_argument('--output', required=True, help ='Path to write file out.')
    parser.add_argument('--vcf-header', required=True, help ='Path to header to put on the vcf.')
    return parser.parse_args()

def main():
    args = get_args()
    convert_ensemb_to_vcf(args.input, args.output, args.vcf_header)

def convert_ensemb_to_vcf(inf, outf, header):

    info_fields = create_base_vcf(outf, header)

    with open(inf, 'r') as f, open(outf, 'a') as o:
        reader = csv.reader(f, delimiter='\t')
        writer = csv.writer(o, delimiter='\t')


        for line in reader:
            chrm = line[0]
            pos = line[1]
            ref, alt = line[3].split('/')

            writer.writerow([chrm, pos, '.', ref, alt, '.', 'PASS', info_fields])

        

def create_base_vcf(file_path, header):
    cp = sp.Popen('cp {header} {fp}'.format(header=header, fp=file_path), shell=True)
    cp.wait()
    info_field = 'RS='
    return info_field



if __name__ == '__main__':
    main()