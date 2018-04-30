import argparse
import os
import pandas as pd
import subprocess as sp


def isolate_allele_frequencies(filepath, extension):
    output_path = filepath.strip(extension) + '_allele_frequencies'
    cmd = '''zgrep -v '^#' {FILENAME} | \
    cut -f8 | \
    cut -d '|' -f1 > {OUT}'''.format(FILENAME=filepath, OUT=output_path)
    proc = sp.Popen(cmd, shell=True)
    proc.wait()
    return output_path


def calculate_allele_frequency_max(path):
    rtn_lst = []
    with open(path) as inf:
        for line in inf:
            onek_pops = line.replace(';', ' ').split()
            print(onek_pops)
            rtn_lst.append(max([float(value.split('=')[1]) for value in onek_pops if '_AF' in value]))
    return rtn_lst


