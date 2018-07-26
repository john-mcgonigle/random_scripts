import argparse
import csv
import time

header = ['chr', 'start',   'stop',    'gene',    'transcript',  'autosomal_recessive', 'autosomal_dominant',
          'x_linked', 'condition']

description = """

A script designed to take in the output of sapientia-task omim_phenotype and return a reformatted .tsv file ready
for uploading to sapientia.

The format required for gene_panel upload is defined as https://sapientia.co.uk/projects#my-projects/A_PROJECT_NO/gene-panel/project/add/upload

It has two arguments:
    The path of the file to be formatted.
    And the path of the file to be outputted.
"""

def args_handler():
    '''
    Function sets up arguments that the script accepts and describes them.
    :return: arguments as a parser object.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input_file', help = 'Path to file to be reformatted prior to upload as a gene panel.', required=True)
    parser.add_argument('-o', '--output_file', help='Path to where the new reformatted file should be stored.', required=True)
    return parser.parse_args()

def categorise_moi(moi_string):
    """
    This function takes in a mode of inheritance (moi) as a string and outputs a list of booleans as integers.
    :param moi_string: A string containing moi information
    :return: A list of integers encoding the mode of inheritance categorically.
    """

    # Set up the defualt values for the variable
    x_linked = False
    autosomal_dominant = False
    autosomal_recessive = False

    # Makes the mode of inhertiance string lowercase
    pattern = moi_string.lower()

    if 'autosomal' in pattern:

        if 'dominant' in pattern:
            autosomal_dominant = True

        if 'recessive' in pattern:
            autosomal_recessive = True

    if 'x' in pattern and 'linked' in pattern:
        x_linked = True

    return [int(autosomal_recessive), int(autosomal_dominant), int(x_linked)]


def reformatter(input_file, output_file):
    """
    :param reader: Reader object containing the file to be reformatted
    :param writer: A writer object through which to output the reformatted file
    :return: None
    """
    with open(input_file, 'r') as input_file, open(output_file, 'w') as output_file:

        reader = csv.reader(input_file, delimiter = '\t')

        # Skip the header row
        next(reader)

        writer = csv.writer(output_file, delimiter = '\t')

        # Write the required header.
        writer.writerow(header)

        for line in reader:

            # Calls a function to convert a string into a list of binary categorise
            # Format returned is something like this [0,1,0]
            moi_categories = categorise_moi(line[4])

            writer.writerow(['', '', '', '', line[1], '',] + moi_categories + [line[3]])

def main():

    # Get the starting time of the script
    start_time = time.time()

    # Store args in a variable to be used in the function
    args = args_handler()

    reformatter(args.input_file, args.output_file)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()