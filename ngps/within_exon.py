import csv
from collections import defaultdict

f = open('SetA.csv')
f1 = open('SetX.csv')
e = open('exon_regions.tsv')

f_reader = csv.reader(f)
f1_reader = csv.reader(f1)
e_reader = csv.reader(e, delimiter='\t')
next(e_reader)

e_dct = defaultdict(dict)
for line in e_reader:
	e_dct[line[0]][line[1]] = line[2]

def contains(x, k, v):
	return x >= k and x <= v

def within_exon(reader, dct):
	i = 0
	l = 0
	next(reader)
	for line in reader:
		l += 1
		i += sum([contains(line[1], k, v) for k,v in dct[line[0]].items()])
	return i, l

within_exon(f_reader, e_dct)
within_exon(f1_reader, e_dct)
		
