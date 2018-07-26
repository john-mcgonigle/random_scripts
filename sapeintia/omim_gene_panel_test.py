import pytest
import csv
import omim_gene_panel_reformatter as reformatter

data_to_categorise = [('x_linked', [0,0,1]),
                      ('Autosomal dominant', [0,1,0]),
                      ('Autosomal recessive', [1,0,0]),
                      ('X_linked, Autosomal_recessive', [1,0,1]),
                      ('X_linked_Autosomal_recessive_Autsomal_Dominant', [1,1,1])]


@pytest.mark.parametrize('data', data_to_categorise)
def test_categorise_moi(data):
    output = reformatter.categorise_moi(data[0])
    assert len(output) == 3
    assert isinstance(output, list)
    assert sum([isinstance(x, int) for x in output]) == 3
    assert data[1] == output


input_file_contents = [['gene_id', 'gene_name', 'omim_phenotype_id', 'omim_phenotype', 'mode_of_inheirtance'],
                       ['1946', 'BCB',	'613065', 'Leukemia, acute lymphocytic, somatic', 'Autosomal_dominant'],
                       ['1945', 'BCR',	'608232', 'Leukemia, chronic myeloid, somatic', 'Autosomal_recessive'],
                       ['10291', 'HOXD13',	'610713', '?Brachydactyly-syndactyly syndrome', 'X_linked'],
                       ['3', 'BII', '61', 'Bad things', 'Autosomal_dominant,x_linked'],
                       ['4', 'KYK', '608', 'REALLY bad things', 'Autosomal_recessive,xlinked,autosomaldominant'],
                       ['1290', 'AREALLYCOOLGENE', '6', 'I am on LITERALLY fire', 'Autosomal Recessive X_linked']]


expected_output_contents = [[['chr', 'start',   'stop',    'gene',    'transcript',
                             'autosomal_recessive', 'autosomal_dominant', 'x_linked', 'condition'],
                            ['', '', '', '', 'BCB',	'', '0', '1', '0', 'Leukemia, acute lymphocytic, somatic'],
                            ['', '', '', '', 'BCR',	'', '1', '0', '0', 'Leukemia, chronic myeloid, somatic'],
                            ['', '', '', '', 'HOXD13', '', '0', '0', '1', '?Brachydactyly-syndactyly syndrome'],
                            ['', '', '', '', 'BII', '', '0', '1', '1', 'Bad things'],
                            ['', '', '', '', 'KYK', '', '1', '1', '1', 'REALLY bad things'],
                            ['', '', '', '', 'AREALLYCOOLGENE', '', '1', '0', '1', 'I am on LITERALLY fire']]]

in_file_path = 'input_tmp.txt'
out_file_path = 'output_tmp.txt'

def reformatter_setup(input, in_path, out_path):
    """
    A function to create a file using the methods to test with which to assess the method functionality and correctness.

    :param input: The input from which we have manually defined an artificial expected output
    :param in_path: Path to writer the input to (as reformatter takes a file)
    :param out_path: Path to write rhte reformatted input to.
    :return:
    """

    # Open a file where to write the contents to be reformatted
    with open(in_path, 'w') as input_to_write:


        writer = csv.writer(input_to_write, delimiter = '\t')

        for line in input:
            writer.writerow(line)

    # Call the function we want to test to produce an output to validate
    reformatter.reformatter(in_path, out_path)

@pytest.mark.parametrize('output', expected_output_contents)
def test_reformatted(output):
    reformatter_setup(input_file_contents, in_file_path, out_file_path)
    with open(out_file_path, 'r') as output_to_check:
        reader = csv.reader(output_to_check, delimiter = '\t')
        for i in xrange(len(output)):
            line = next(reader)
            print(line)
            print(output[i])

            assert output[i] == line



