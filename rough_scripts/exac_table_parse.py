import sys
import csv
import gzip
import io
import os
sod1_start = 33030000
sod1_end = 33042200


def get_region_of_interest(input_path, output_path, delim=','):
	with gzip.open(input_path, 'rb') as gz_file, open(output_path, 'w') as o:
	    f = io.BufferedReader(gz_file)
	    writer = csv.writer(o, delimiter = delim)
	    # print(next(f).split('\t'))
	    line = next(f)
	    line = line.split('\t')
	    writer.writerow(line)

	    for line in f:
	    	line = line.split('\t')
	    	if int(line[0]) == 21:
	    		# print(int(line[1]))
	    		if int(line[1]) > sod1_start and int(line[1]) < sod1_end:
	    			writer.writerow(line)

	    	if int(line[0]) == 22:
	    		break

def get_variants(input_path, output_path, func, header=None, delim=',', skip_header = False, info = None):
	with open(input_path, 'r') as f, open(output_path, 'w') as o:
		reader = csv.reader(f, delimiter= delim)
		writer = csv.writer(o, delimiter= '\t')

		if skip_header:
			next(reader)

		if info is not None:
			for line in info:
				writer.writerow([line])

		if header is not None:
			writer.writerow(header)

		for line in reader:
			# print(line)
			rtn = func(line)
			if type(rtn) is dict:
				for key in rtn:
					writer.writerow(rtn[key])
			else:
				writer.writerow(rtn)
				

def parse_dbsnp(line):
	db = 'db_snp'
	sap_id = ''
	rsID = line[2]
	chrm = line[0]
	pos = line[1]
	ref = line[3]
	alt = line[4]
	info = line[7]

	consequence = ''
	clin_sig = ''

	gene_name = mangle_string(info, 'GENEINFO=', ':')
	rtn = [db, gene_name, sap_id, chrm, pos, ref, alt, consequence, clin_sig, rsID]
	rtn += ['']*4

	return rtn

def parse_ensemble(line):
	rtn = {}
	i = 1
	# print(line)
	db = line[9]
	sap_id = ''
	if line[0][:2] == 'rs':
		rsID = line[0]
	else:
		rsID = ''
	chrm = line[2].split(':')[0]
	pos = line[2].split(':')[1]

	consequence = line[11]
	clin_sig = line[10]

	if type(line[16]) is float:
		sift_score = line[16]
		sift_signif = line[15]
	else:
		sift_score = ''
		sift_signif = ''

	if type(line[19]) is float:
		polyPhen_score = line[19]
		polyPhen_signif = line[18]
	else:
		polyPhen_score = ''
		polyPhen_signif = ''

	gene_name = 'SOD1'

	alleles = line[5].split('/')
	ref = alleles[0]
	if len (alleles)<2:
		return [db, gene_name, sap_id, chrm, pos, ref, '', consequence, clin_sig, rsID, sift_score, sift_signif, polyPhen_score, polyPhen_signif]
	elif len(alleles) > 2: 
		for allele in alleles[1:]:
			rtn[i] = [db, gene_name, sap_id, chrm, pos, ref, allele, consequence, clin_sig, rsID, sift_score, sift_signif, polyPhen_score, polyPhen_signif]
			i += 1
		return rtn
	else:
		return [db, gene_name, sap_id, chrm, pos, ref, alleles[1], consequence, clin_sig, rsID, sift_score, sift_signif, polyPhen_score, polyPhen_signif]
		


def parse_exac(line):
	db = 'ExAC'
	sap_id = ''
	chrm = line[0]
	pos = line[1]
	ref = line[2]
	alt = line[3]
	consequence = line[63]
	gene_name = line[57]
	clin_sig = line[46]
	rsID = ''

	if line[67] == 'SIFT':
		sift_signif, sift_score,  = 'sift_prediction', 'sift_score'
		polyPhen_signif, polyPhen_score,  = 'polyPhen_prediction', 'polyPhen_score'
	else:
		sift_signif, sift_score,  = parse_scores(line[67])
		polyPhen_signif, polyPhen_score,  = parse_scores(line[68])

	return [db, gene_name, sap_id, chrm, pos, ref, alt, consequence, clin_sig, rsID, sift_score, sift_signif, polyPhen_score, polyPhen_signif]


def parse_scores(score):
	if score != 'NA':
		score = score.split('(')
		return score[0], score[1][:-1]
	else:
		return score, score


def mangle_string(item, pattern, splitter, modifier=0):
	return item[item.find(pattern) + len(pattern) + modifier:].split(splitter)[0]


def dblist_vcf_conversion(line):
	vcf_line = line[3:5]+['.']+line[5:7]+['.']+['.']+['.']
	return vcf_line

def create_info_field(line):
	print(line)
	vep = line[7]
	sift_score = line[10]
	sift_pred = line[11]
	poly_score = line[11]
	poly_pred = line[12]
	clin_sig = line[8]
	evidence = line[15]
	description = line[16]
	fields = [vep, sift_score, sift_pred, poly_score, poly_pred, clin_sig, evidence, description]
	labels = ['VEP', 'SS', 'SP', 'PS', 'PP', 'CS', 'ALS', "EVIDENCE"]
	rtn = [k+'='+v for k,v in zip(labels, fields)]

	return ';'.join(rtn)



def curated_list_vcf_conversion(line):
	vcf_line = line[3:5]+['.']+line[5:7]+['.']+['.']
	info = create_info_field(line)
	return vcf_line + [info]


exac_table = '/Users/john.mcgonigle/work_dir/data/ExAC.r1.sites.vep.table.gz'
chrom21 = '/Users/john.mcgonigle/work_dir/data/chr21_table.vcf'
sod1_exac = '/Users/john.mcgonigle/work_dir/data/sod1_exac.vcf'

db_vcf = '/Users/john.mcgonigle/work_dir/data/dbSNP_SOD1_NH.vcf'
sod1_db = '/Users/john.mcgonigle/work_dir/data/sod1_variants_dbSNP.vcf'

vcf_header = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']

sod1_superlist = '/Users/john.mcgonigle/Documents/Projects/Biogen/subsets/sod1_QC.csv'
sod1_superlist_vcf = '/Users/john.mcgonigle/work_dir/data/sod1_superlist.vcf'

ensembl = '/Users/john.mcgonigle/Documents/Projects/Biogen/subsets/ensembl-export.csv'
ensemble_cleaned = '/Users/john.mcgonigle/Documents/Projects/Biogen/subsets/ensembl-export-processed.csv'

vcf_info_format = '##INFO=<Format: VEP_CONSEQUENCE|SIFT_SCORE|SIFT_PREDICTION|POLYPHEN_SCORE|POLYPHEN_PREDICTION|CURATED_SIGNIFICANCE|EVIDENCE">'

file_format = '##fileformat=VCFv4.1'
vep = "##INFO=<ID=VEP,Number=1,Type=String,Description='VEP_CONSEQUENCE'>"
sift_score = "##INFO=<ID=SS,Number=1,Type=Float,Description='SIFT_SCORE'>"
sift_pred = "##INFO=<ID=SP,Number=1,Type=String,Description='SIFT_PREDICTION'>"
poly_score = "##INFO=<ID=PS,Number=1,Type=Float,Description='SIFT_SCORE'>"
poly_pred = "##INFO=<ID=PP,Number=1,Type=String,Description='SIFT_PREDICTION'>"
clinical_sig = "##INFO=<ID=CS,Number=1,Type=String,Description='CLINICAL_SIG'>"
signif = "##INFO=<ID=ALS,Number=1,Type=String,Description='ALS_SIGNIFICANCE'>"
evid = "##INFO=<ID=EVIDENCE,Number=1,Type=String,Description='EVIDENCE_SUPPLIED'>"

vcf_rubbish = [file_format, vep, sift_score, sift_pred, poly_score, poly_pred, clinical_sig, signif, evid]

curated_lst = '/Users/john.mcgonigle/Documents/Projects/Biogen/sod1_curated_variants.csv'
curated_lst_vcf = '/Users/john.mcgonigle/Documents/Projects/Biogen/sod1_curated_variants.vcf'

# get_region_of_interest(exac_table, chrom21, delim = '\t')	
# get_variants(chrom21, sod1_exac, parse_exac, delim = '\t')
# get_variants(db_vcf, sod1_db, parse_dbsnp, delim = '\t')
# get_variants(ensembl, ensemble_cleaned, parse_ensemble, delim = ',', skip_header = True)
# get_variants(sod1_superlist, sod1_superlist_vcf, dblist_vcf_conversion, delim=',', skip_header = True)
get_variants(curated_lst, curated_lst_vcf, curated_list_vcf_conversion, header = vcf_header, skip_header = True, info = vcf_rubbish, delim = '\t')



