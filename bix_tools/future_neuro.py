import subprocess as sp
import os 
import time
import csv
import sys
from collections import defaultdict

path_to_ir_csv = '/sftp_data/robcarton_futureneuro/Uploads/For_Transfer_to_Congenica'
current_dir = '/sftp_data/robcarton_futureneuro/'
vcf_file_dir = '/sftp_data/robcarton_futureneuro/vcfs'


def make_ir_csv(path, outpath, file_dct):
    samples_dct = defaultdict(dict)
    with open(path, 'r') as in_csv, open(outpath, 'w') as out_csv:
        reader = csv.reader(in_csv)
        writer = csv.writer(out_csv)

        header = next(reader)

        writer.writerow(header)

        for line in reader:
            if line[0] in file_dct:
                line[12] = file_dct[line[0]]
                writer.writerow(line)


def move_files_to_single_dir(path, final_dest):
    folders = [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item)) and item not in ['Uploads', 'vcfs']]
    sample_files = defaultdict(str)

    for folder in folders:
        sample = folder.split('_')[0]
        if '-rpt' in sample:
            sample = sample.strip('-rpt')


        filepath = os.path.join(path, folder, sample+'.vcf')
        proc = sp.Popen('cp ' + filepath +' ' + os.path.join(final_dest, sample+'.vcf'), shell=True)
        proc.wait()

        sample_files[sample] = filepath

    return sample_files


        
def main():
    file_dct = move_files_to_single_dir(current_dir, vcf_file_dir)
    make_ir_csv(os.path.join(path_to_ir_csv, 'project_733_ir_initial91.csv'), os.path.join(path_to_ir_csv, 'project_733_ir_processed_90.csv'), file_dct)



if __name__ == '__main__':
    main()










