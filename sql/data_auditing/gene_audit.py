import csv
import argparse
from collections import namedtuple


EnsemblGeneRecord = namedtuple('EnsemblGeneRecord',('start', 'end'))

def load_ensembl_gene_to_dictionary(path):
    ens_gene_dct = {}
    # print(path)
    with open(path, 'r') as inf:
        reader, header = _return_csv_reader(inf)
        for line in reader:
            try:
                ens_gene_dct[line[0]] = EnsemblGeneRecord(start=int(line[1]), end=int(line[2]))
            except:
                ens_gene_dct[line[0]] = EnsemblGeneRecord(start=None, end=None)

    return ens_gene_dct

def gene_validation(ens_gene_dct, in_path, out_path):
    with open(in_path, 'r') as inf, open(out_path, 'w') as out:
        reader, header = _return_csv_reader(inf)
        header += ['ens_start', 'ens_end']
        writer = csv.writer(out)
        writer.writerow(header)

        for line in reader:
            try:
                ESG_id, start, end = line[-1], int(line[2]), int(line[3])
            except:
                print(line)
                
            if ESG_id in ens_gene_dct:
                if ens_gene_dct[ESG_id].start is not None:
                    if (ens_gene_dct[ESG_id].start == start) and ( end == ens_gene_dct[ESG_id].end):
                        pass
                    else:
                        writer.writerow(line + [ens_gene_dct[ESG_id].start, ens_gene_dct[ESG_id].end])
                else:
                    print(line)

def _return_csv_reader(file_obj):
        reader = csv.reader(file_obj)
        header = next(reader) # Skip header line
        return reader, header

def gene_audit():

    description = '''A script to validate that gene coordinates are the same as in ensembl and return those that aren\'t'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('path_to_ensembl_gene_definitions', type=str, help = 'The path to the export of gene definitions')
    parser.add_argument('path_to_gene', type=str, help = 'The path to the export of exon boundaries')
    parser.add_argument('path_to_gene_audit', type=str, help = 'The path to output the audit report')
    args = parser.parse_args()

    gene_dct = load_ensembl_gene_to_dictionary(args.path_to_ensembl_gene_definitions)
    gene_validation(gene_dct, args.path_to_gene, args.path_to_gene_audit)
    # print(gene_dct)

if __name__ == '__main__':
    gene_audit()