import csv


def file_get(path, file_type):
	f = open(path, file_type)
	return f


def get_reader(infile, skip, delimiter):
	reader = csv.reader(infile, delimiter = delimiter)

	if skip:
		next(reader)

	return reader


def get_writer(infile):
	writer = csv.DictWriter(infile, fieldnames = table_header, lineterminator = '\n', delimiter = ',')
	writer.writeheader()
	return writer


def parse_als_variant_server(line):
	rtn = ['als_variant_server', # db
	 line[2], # gene name
	  line[0].strip('chr'), # chrmsm
	   line[1], # pos
	     line[7], # ref
	      line[8], # alt
	          line[4], # var type
	            '', # condition
	             line[17], # predicted signif
	              line[5] # var id
	              ]
	return return_dict(rtn)

# def get_index(item):
# 	for i in range(1, len(item)):
# 		if type(item[-i]) if int:
# 			return -i


def parse_clinvar(line):
	rtn = ['clinVar', # db
	 line[1], # gene name
	  line[5], # chrmsm
	   line[6], # pos
	     '', # ref
	      '', # alt
	          '', # var type
	            line[2], # condition
	             line[3], # predicted signif
	              '' # var id
	              ]
	return return_dict(rtn)

def parse_alsod_db(line):
	chrmsm, pos = field_split(line[13], ':')
	rtn = ['alsod_db', # db
	 line[2], # gene name
	  chrmsm, # chrmsm
	   pos, # pos
	     line[4][0], # ref
	      line[5][0], # alt
	          line[9] + ' ' + line[3], # var type
	            '', # condition
	             '', # predicted signif
	              line[14] # var id
	              ]
	return return_dict(rtn)

def field_split(item, split_by):
	info= item.split(split_by)
	if len(info)>1:
		chrmsm = info[0]
		pos = info[1]
	else:
		chrmsm = ''
		pos = ''
	return chrmsm, pos


def parse_als_gene(line):
	chrmsm, pos = field_split(line[1], ':')
	chrmsm.strip('chr')
	ref, alt = field_split(line[6], 'vs.')

	rtn = ['als_gene', # db
	 line[2], # gene name
	  chrmsm, # chrmsm
	   pos, # pos
	     ref, # ref
	      alt, # alt
	          '', # var type
	            '', # condition
	             '', # predicted signif
	              line[0] # var id
	              ]
	return return_dict(rtn)


def return_dict(lst):
	return {k:v for k,v in zip(table_header, lst)}


# def parse_dbSnp(line):
# 	if len(line)>0:
# 		line = line[0].split(']')
# 		rsID = line[0].split(' ')[0]
# 		line = line[1].split(' ')
		

# 		gene_name = line[10]
# 		if len(gene_name)>4:
# 			gene_name = gene_name[-4:]

# 		signif = line[20]
		
# 		if signif in ['Likely', 'Uncertain']:
# 			signif += ' ' + line[21]
# 			alt = line[23].split(':')
# 			if alt  not in ['A', 'T', 'G', 'C']:
# 				print(line)

# 		else:
# 			alt = line[23].split(':')

		

# 		rtn = ['db_snp', # db
# 		 gene_name, # gene name
# 		  line[6], # chrmsm
# 		   line[9], # pos
# 		     '', # ref
# 		      alt[0], # alt
# 		       '', # amino acid
# 		        '', # aa orignial
# 		         '', # aa mut
# 		          '', # var type
# 		            '', # condition
# 		             signif, # predicted signif
# 		              rsID # var id
# 		              ]
# 		return return_dict(rtn)


def file_parser(reader, writer, key):
	for line in reader:
		dct = func_dict[key][0](line)
		if dct is not None:
			writer.writerow(dct)


def main(outpath):
	
	outf = file_get(outpath, 'w')
	writer = get_writer(outf)

	for db in file_lst:

		path = file_dict[db]

		handle_file(writer, path, db)

	outf.close()

def handle_file(writer, path, key):
	infile = file_get(path, 'r')
	reader =get_reader(infile, func_dict[key][1], func_dict[key][2])
	file_parser(reader, writer, key)
	infile.close()

table_header = ['DB_origin',	'Gene_name',	'Chromosome',	'Position',	'Reference',	'Alternative',	
				'Variant_type',	'Condition', 'Predicted_significance', 'rsID']

file_dict = {'clinVar': '/Users/john.mcgonigle/Documents/Projects/Biogen/subsets/Clivar_SOD_ALS.csv',
				'alsod_db': '/Users/john.mcgonigle/Documents/Projects/Biogen/subsets/alsod_db.csv',
				'als_gene': '/Users/john.mcgonigle/Documents/Projects/Biogen/subsets/alsgene_SOD.csv',
				'als_variant_server': '/Users/john.mcgonigle/Documents/Projects/Biogen/subsets/ALS_variant_server_SOD1.csv'}
				
file_lst = ['clinVar', 'alsod_db', 'als_gene', 'als_variant_server']


func_dict = {'clinVar': [parse_clinvar, True, ','],
				'alsod_db': [parse_alsod_db, True, ','],
				'als_gene': [parse_als_gene, True, ','],
				'als_variant_server': [parse_als_variant_server, True, ',']}

out_path = '/Users/john.mcgonigle/Documents/Projects/Biogen/subsets/aggregated_data.csv'

if __name__ == '__main__':
	main(out_path)
