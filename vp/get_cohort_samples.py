import gzip
import io
import os
import csv

os.chdir('/scratch/data/oneK_genomes/vcf/')

def load_sample_ids(path):

	with open(path, 'r') as f:
		lst = []
		males = []
		reader = csv.reader(f)
		next(reader)

		for line in reader:

			lst += [line[0]]
			if line[1] == 'male':
				males += [line[0]]

	return lst, males

def get_files():
	path_lst = []
	for path in os.listdir():
		if path[-3:] == '.gz':
			path_lst += [path]
	return path_lst


def handler_function():
	file_lst = get_files()
	for file_path in file_lst:
		sample_vcf(file_path, '_cohort')


def sample_vcf(input_path, id, delim='\t'):
	output_path = input_path[:15]+id+'.vcf'
	with gzip.open(input_path, 'rt') as gz_file, open(output_path, 'w') as o:

	    # f = io.BufferedReader(gz_file)
	    writer = None
	    # print(next(f).split('\t'))

	    idxs = [i for i in range(9)]

	    if 'Y' in input_path:
	    	print(input_path)
	    	samples_to_use = male_ids
	    else:
	    	samples_to_use = sample_ids

	    for line in gz_file:
	    	if '##' in line:
	    		o.write(line)
	    	else:
	    		
	    		if writer == None:
	    			writer = csv.writer(o, delimiter = delim)

	    		# print(line)
	    		line = line.split('\t')
	    		if line[0] == '#CHROM':
	    			idxs += get_indexes(line, samples_to_use)
	    			row = [line[i] for i in idxs]
	    			writer.writerow(row)
	    		else:
	    			row = [line[i] for i in idxs]
	    			writer.writerow(row)
	    # 		writer.writerrow([line[i] for i in idxs])


def get_indexes(line, samples_to_use):
	print(sample_ids)
	rtn = [line.index(sample_id) for sample_id in samples_to_use]
	return rtn 


cohort = '/scratch/data/oneK_genomes/vcf/cohort_1/cohort_1_sample_lst.csv'
# gzf = 'ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz'
sample_ids, male_ids = load_sample_ids(cohort)
print(sample_ids)
# sample_vcf(gzf, '_cohort')
handler_function()
