import argparse as ap
import csv
import json

def define_args():
    parser = ap.ArgumentParser(description='A script to load specific panel specified by gel into the database.')
    parser.add_argument('--panels', required=True,
                        help='The path to the file containing panels')
    parser.add_argument('--output-json', required=True,
                        help='The json file to output the contents to.')
    return parser.parse_args()

def parse_file(reader):
    rtn_lst = []
    next(reader) # skip the header
    for line in reader:
        rtn_lst.append({"specificDisease":line[0],
                        "panelName":line[1],
                        "panelVersion":line[2]})
    return rtn_lst




def main():
    args = define_args()
    with open(args.panels) as inf, open(args.output_json, 'w') as out:
        reader = csv.reader(inf)
        json_data = parse_file(reader)
        json.dump(json_data, out)

if __name__ == '__main__':
    main()

        