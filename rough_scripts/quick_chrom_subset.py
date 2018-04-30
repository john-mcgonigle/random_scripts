import sys
import csv
import zipfile



csv.field_size_limit(sys.maxsize)

def chrom_subset(reader):

		for line in reader:
			if line[0] == '21':
				writer.writerow(line)

			if line[0] == '22':
				break

def get_gene(start, end, reader, writer):
	# i = 0
	# while i <10:
	# 	line = next(reader)
	# 	print(line[1])
	# 	i += 1
	for line in reader:
		if int(line[1]) > start and int(line[1]) < end:
			writer.writerow(line)


path = '/Users/john.mcgonigle/work_dir/data/ExAC.vcf'
chrom_path = '/Users/john.mcgonigle/work_dir/data/chr21.vcf'
sod1 = '/Users/john.mcgonigle/work_dir/data/get_gene.vcf'

# chrom_subset(path, outpath)

def run_subset(path, outpath, delim = ','):
	with open(path, 'r') as f, open(outpath, 'w') as o:
		reader = csv.reader(f, delimiter = delim)
		writer = csv.writer(o)
		get_gene(33031935, 33041244 , reader, writer)

# run_subset(chrom_path, sod1)

def show_few(path, delim = ','):
	with open(path, 'r') as f:
		reader = csv.reader(f, delimiter = delim)
		# line = next(reader)
		line = format_line(next(reader))

		print(line)

def format_line(line):
	chrm = line[0]
	pos = line[1]
	ref = line[3]
	alt = line[4]
	consequence = mangle_string(line[7], 'CSQ='+alt, 6)
	rsID = mangle_string(line[7], 'rs', 0)
	gene_name = mangle_string(line[7], 'MODIFIER', 9)
	return ([chrm, pos, ref, alt, rsID, gene_name, consequence])

def mangle_string(item, pattern, modifier):
	return item[item.find(pattern) + modifier:].split('|')[0]

# show_few(sod1)

