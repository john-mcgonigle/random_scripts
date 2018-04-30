import json
import csv
import os
from pprint import pprint

# print(os.listdir())
json_path ='/Users/john.mcgonigle/work_dir/data/sod1_superlist.vcf.vep.json'

def vep_json_to_superlist(file_path, out_path):

    with open(file_path, 'r') as f, open(out_path, 'w') as o:

        writer = csv.writer(o, delimiter =',')

#         line = json.loads(next(f))
#         pprint(line)

        for line in f:
            line_to_write = line_parser(line)
            writer.writerow(line_to_write)


def line_parser(line):
            
    line = json.loads(line)
    start = line['start']
    alleles = line['allele_string'].split('/')
    ref = alleles[0]
    alt = alleles[1]
    chrm = line['seq_region_name']
            
    if 'transcript_consequences' in line:
        transcript = line['transcript_consequences'][0]
        if 'hgvsc' in transcript:
            hgvsc = transcript['hgvsc']
        else:
            hgvsc = ''
#     #         pprint(transcript)

    else:
        transcript = line['intergenic_consequences'][0]
        hgvsc = ''

    if 'sift_score' in transcript:
        sift_score = transcript['sift_score']
        sift_prediction = transcript['sift_prediction']
        polyPhen_score = transcript['polyphen_score']
        polyPhen_prediction = transcript['polyphen_prediction']
    
    else:
        sift_score = ''
        sift_prediction = ''
        polyPhen_score = ''
        polyPhen_prediction = ''

    consequence = ', '.join(transcript['consequence_terms'])
    vep_impact = transcript['impact']
            
    rtn = [chrm, start, ref, alt, consequence, sift_score, sift_prediction, polyPhen_score,
                   polyPhen_prediction, vep_impact, hgvsc]
    return rtn
            

vep_json_to_superlist(json_path, json_path[:-13]+'.csv')