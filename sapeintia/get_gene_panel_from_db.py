import os
import csv
import argparse

import psycopg2.extras

description = """
    get_gene_panel_from_db

    This script is designed to take in a output path (for the csv) and a gene panel id from sapientia's DB and write out
    the contents of the gene panel into a csv. This csv is produced in the format of the Congenica gene panel upload
    specifications and thus can either be posted to a db using the uplaod script or uploaded manually through the website.

    It takes two input arguments:
    outpath: the path to write the resultant csv file
    panel_id: the sapinetia databse id of the panel to be outputted.

    The intended function of this script was to enable ease of movement of gene panels between different sapientia instances.

    Note if running this outside of Docker then the following environmental variables will need to be manually set in your terminal:
    SAPIENTIA_DB_HOST,
    SAPIENTIA_DB_NAME,
    SAPIENTIA_DB_USER,
    SAPIENTIA_DB_PASSWORD

"""

# The header to use in producing the csv. Note that this is required, non-felxible, and taken driectly from the upload gene panels section
header = ['chr', 'start', 'stop', 'gene', 'transcript', 'autosomal_recessive', 'autosomal_dominant', 'x_linked', 'condition']


class SapientiaDB(object):
    """
    A class object to handle the connection to the database and the mangement of queries in the database
    It requires no arguments to be initialised.
    """
    def __init__(self):
        self.db = self._get_cursor()

    def _get_cursor(self):
        """
        Sets up a connetion with the sapientia database.

        Note if running this outside of Docker then the following environmental variables will need to be manually set in your terminal:
        SAPIENTIA_DB_HOST,
        SAPIENTIA_DB_NAME,
        SAPIENTIA_DB_USER,
        SAPIENTIA_DB_PASSWORD

        :return: a Dict cursor allowing access to the column values explicitly via the column names
        """
        connect_str = "host={SAPIENTIA_DB_HOST} dbname={SAPIENTIA_DB_NAME} user={SAPIENTIA_DB_USER} password={SAPIENTIA_DB_PASSWORD}".format(**os.environ)
        conn = psycopg2.connect(connect_str)

        # psycopg2.extras.DictCursor returns a list of dictionaries where the keys are the column names
        # thus the column values can be accessed explicitly.
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        return cur

    def _get_query(self, query, arg):
        """
        A function that acts as a query builder. Takes in a query as an argument and a single item tuple and produces a
        valid query and executes it returning the results.

        :param query: The SQL query to executed
        :param arg: A argument by which to reduce the query results e.g. panel_id in the format of a single item tuple
         the reason for this typing is because we're utilising db.execute's magic string management to avoid SQL injection

        :return: entries - a list of dictionaries resulting from the query
        """
        query += " %s"
        self.db.execute(query, arg)
        entries = self.db.fetchall()

        return entries

    def get_gene_panel(self, gene_panel_id):
        return self._get_query("SELECT * FROM gene_to_gene_panel where gene_panel_id=", (gene_panel_id, ))

    def convert_gene_panel_to_dict(self, db_contents):
        """
        A function to collect and aggregate the contents of a gene_panel from one Sapientia DB instance.

        :param db_contents: The contents of a query against gene_to_gene_panel for the specific gene_panel we're interested in.
        :return: entry_lst: A list of dictionaries where each record is valid input for the csv writer.
        """

        entry_lst = []

        # For every gene in the gene panel collect the information.
        for gene in db_contents:

            gene_id = gene['gene_id']
            transcript_id = gene['transcript_id']

            # Gather the gene table information for each gene.
            gene_info = self._get_query("SELECT * FROM gene where gene_id=", (str(gene_id), ))[0]

            # Get the transcript name from the transcript id.
            transcript = self._get_query("SELECT * FROM transcript where transcript_id=", (str(transcript_id), ))[0][2]

            # Dictionary of values to be written out in the .csv
            entry = {'chr':gene_info['chr'],
                        'start':gene_info['start'],
                        'stop':gene_info['end'],
                        'transcript': transcript,
                        'autosomal_recessive':int(gene['autosomal_recessive']),
                        'autosomal_dominant': int(gene['autosomal_dominant']),
                        'x_linked':int(gene['x_linked']),
                        'condition': gene['condition']}

            # Casting the inheritance values to int because otherwise they get returned as booleans.

            entry_lst.append(entry)

        return entry_lst


def get_args():

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-o', '--output-path', required=True, help='Path to the csv you wish to be outputted')
    parser.add_argument('-id', '--gene-panel-id', required=True, help = 'A gene panel id for the intended sapientia db')
    return parser.parse_args()

def write_gene_panel_dict_to_csv(panel_dct, outpath):
    """
    Takes in a list of dictionaries and iterates through each entry in the list writing out the contents into a file.
    :param panel_dct: List of dictionaries
    :param outpath: Path to sv to be written
    :return:
    """
    with open(outpath, 'w') as outf:
        writer = csv.DictWriter(outf, fieldnames=header)
        writer.writeheader()

        for entry in panel_dct:
            writer.writerow(entry)

def main():
    # Set up connection
    db_connection = SapientiaDB()

    # Get arguments
    args = get_args()

    # Get panel information
    panel = db_connection.get_gene_panel(args.gene_panel_id)

    # Collect gene information for all genes in the panel
    entries = db_connection.convert_gene_panel_to_dict(panel)

    # Write out the panel as a csv
    write_gene_panel_dict_to_csv(entries, args.output_path)


if __name__ == '__main__':
    main()
