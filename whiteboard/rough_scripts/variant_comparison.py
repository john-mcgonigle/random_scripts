import argparse
import csv
import datetime as dt

description =""" This script takes two files, creates a list containing the variants 
and then outputs a file consisting of lines of the second file that are not in the first """

def get_files():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('function', help = 'Function to run, diff/intersect.')
    parser.add_argument('file_one', help = 'A path to the the first file to load.')
    parser.add_argument('file_two', help='A path to the second file to load.')
    parser.add_argument('out_path', help='A path to the file to output.')

    parser.add_argument('--sep1', type=str, default=',', help='Delimiter of file 1.')
    parser.add_argument('--sep2', type=str, default=',', help='Delimiter of file 2.')

    args = parser.parse_args()

    f1 = open(args.file_one, 'r')
    f2 = open(args.file_two, 'r')
    reader1 = csv.reader(f1, delimiter = args.sep1)
    reader2 = csv.reader(f2, delimiter = args.sep2)
    return f1, f2, reader1, reader2, args

def make_unique_variant_key(line):
    return str(line[1]) + '_'+''.join(line[2:4])

def make_variant_dct(reader):
    next(reader)
    rtn_dct = {make_unique_variant_key(line):[line[1:4]] for line in reader}
    return rtn_dct

def make_hgmd_dct(reader):
    next(reader)
    for line in reader:
        rtn_dct = {make_unique_variant_key(line):line[-4:-1] for line in reader}
    return rtn_dct

def get_difference(outpath, reader, dct):
    with open(outpath, 'w') as out:

        writer = csv.writer(out)
        writer.writerow(next(reader))

        for line in reader:

            if make_unique_variant_key(line) in dct:
                pass

            else:
                writer.writerow(line)

def intersect_files(outpath, reader, dct):
       with open(outpath, 'w') as out:
        observed = []

        writer = csv.writer(out)
        writer.writerow(next(reader))

        for line in reader:
            key = make_unique_variant_key(line)
            if key in dct:
                line += dct[key]
                observed.append(key)
            writer.writerow(line)

        un_observed = list(set(dct.keys()) - set(observed))
        if len(un_observed)>=1:
            print(un_observed)


def main():
    open_f1, open_f2, r1, r2, args = get_files()
    out = args.out_path

    if args.function == 'difference':
        variant_dct = make_variant_dct(r1)
        get_difference(out, r2, variant_dct)

    if args.function == 'intersect':
        hgmd_dct = make_hgmd_dct(r2)
        intersect_files(out, r1, hgmd_dct)

    open_f1.close()
    open_f2.close()

main()
