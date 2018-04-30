import csv
import argparse
from collections import namedtuple


GeneRecord = namedtuple('GeneRecord',('start', 'end', 'name', 'gene_id'))

def load_genes_to_dictionary(path):
    gene_dct = {}
    # print(path)
    with open(path, 'r') as inf:
        reader, header = _return_csv_reader(inf)

        for line in reader:
            try:
                gene_dct[line[0]] = GeneRecord(start=int(line[2]), end=int(line[3]), name=line[1], gene_id=line[-1])
            except:
                gene_dct[line[0]] = GeneRecord(start=None, end=None, name=None, gene_id=None)

    return gene_dct

def exon_validation(gene_dct, in_path, out_path):
    with open(in_path, 'r') as inf, open(out_path, 'w') as out:
        reader, header = _return_csv_reader(inf)
        header = ['gene_name', 'gene_ensembl_id'] + header
        writer = csv.writer(out)
        writer.writerow(header)

        for line in reader:
            GID, start, end = line[0], int(line[3]), int(line[4])
            if gene_dct[GID].start is not None:
                if (gene_dct[GID].start <= start <= gene_dct[GID].end) and ( gene_dct[GID].start <= end <= gene_dct[GID].end):
                    pass
                else:
                    writer.writerow([gene_dct[GID].name, gene_dct[GID].gene_id] + line)
            else:
                print(line)

def _return_csv_reader(file_obj):
        reader = csv.reader(file_obj)
        header = next(reader) # Skip header line
        return reader, header

def audit():

    description = '''A script to validate that exons are all within genes and return those that aren\'t'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('path_to_genes', type=str, help = 'The path to the export of gene definitions')
    parser.add_argument('path_to_exons', type=str, help = 'The path to the export of exon boundaries')
    parser.add_argument('path_to_audit', type=str, help = 'The path to output the audit report')
    args = parser.parse_args()

    gene_dct = load_genes_to_dictionary(args.path_to_genes)
    exon_validation(gene_dct, args.path_to_exons, args.path_to_audit)
    # print(gene_dct)

if __name__ == '__main__':
    audit()