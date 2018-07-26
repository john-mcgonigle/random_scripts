import argparse
import csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in_path', default=True)
    parser.add_argument('-o', '--out_path', default=True)
    args = parser.parse_args()

    with open(args.in_path, 'r') as inf, open(args.out_path, 'w') as outf:
        remove_character(inf, outf, "\xef\xbb\xbf")

def remove_character(inf, outf, pattern):
    reader = csv.reader(inf)
    writer = csv.writer(outf)

    for line in reader:
        newline = [item.strip(pattern) for item in line]
        writer.writerow(newline)

if __name__ == '__main__':
    main()

