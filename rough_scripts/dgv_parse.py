import sys
import csv

def run_subset(path, outpath, pattern, delim = ','):
	with open(path, 'r') as f, open(outpath, 'w') as o:
		reader = csv.reader(f, delimiter = delim)
		writer = csv.writer(o, delimiter = delim)
		# print(next(reader))

		if pattern == 0:
			get_chrom(reader, writer)
		elif pattern == 1:
			extract_details(reader, writer)

def get_chrom(reader, writer):
	for line in reader:
		if line[0][3:] == '21':
			line_parse(line, writer)
		elif line[0][3:] == '22':
			break

def line_parse(line, writer):
	l_start = int(line[3])
	l_end = int(line[4])

	if l_start < start and l_end > start:
		writer.writerow(line)
	elif l_start > start and l_start < end:
		writer.writerow(line)

def extract_details(reader, writer):
	for line in reader:
		db = 'DGV'
		chrm = line[0][3:]
		gene = 'SOD1'
		pos = line[3]
		vtype = mangle_string(line[8], 'variant_type=', ';', 0)
		v_sub_type = mangle_string(line[8], 'variant_sub_type=', ';', 0)
		consequence = vtype + ' ' + v_sub_type + ' (' + line[3] + '-' + line[4] + ')'

		rtn = [db, gene, '', chrm, pos, consequence]
		rtn += ['']*8
		# print(rtn)

		writer.writerow(rtn)

def mangle_string(item, pattern, splitter, modifier):
	return item[item.find(pattern) + len(pattern) + modifier:].split(splitter)[0]


dvg_file = '/Users/john.mcgonigle/work_dir/data/DGV.GS.March2016.50percent.GainLossSep.Final.hg19.gff3'
dgv_chrom_file = '/Users/john.mcgonigle/work_dir/data/DGV_chrom21.csv'
dgv_sod_file = '/Users/john.mcgonigle/work_dir/data/DGV_sod1.csv'

start = 33030000
end = 33042000

run_subset(dvg_file, dgv_chrom_file, 0, '\t')
run_subset(dgv_chrom_file, dgv_sod_file, 1, '\t')
