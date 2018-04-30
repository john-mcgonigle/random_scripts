
import csv

distance = 50
gap = 1000000

inf = '/Users/john.mcgonigle/work_dir/data/exac_release_1.0/count_of_var.csv'
outf = '/Users/john.mcgonigle/work_dir/data/exac_release_1.0/variant_score_per_locus.csv'

def get_conservation_score(input_path, output_path, delim=','):

	with open(input_path, 'r') as f, open(output_path, 'w') as o:
		reader = csv.reader(f)
		next(reader)
		writer = csv.writer(o)
		writer.writerow(['Chrom', 'Position', 'Score', 'Plot_location'])

		values_dct = make_chrom_dct(reader)

		print('Dict stocked')

		chromosomes = get_sorted_keys(values_dct)

		plot_location = None

		for chrm in chromosomes:
			print(chrm)
			positions = [int(val) for val in values_dct[chrm].keys()]
			positions.sort()
			
			previous = positions[0]

			if plot_location is None:
				plot_location = positions[0]

			for i in range(len(positions)):
				upper = i + distance
				lower = i - distance 

				if i < distance:
					keys = positions[:i] + positions[i: upper + 1]

				elif i < (len(positions) - distance):
					keys = positions[lower: upper + 1]

				else:
					keys = positions[lower:]

				current = positions[i]
				upper = int(current) + distance
				lower = int(current) - distance

				values = [int(values_dct[chrm][str(key)]) for key in keys if key >= lower and key <= upper]

				score = sum(values)
				score = float(score)/(distance*2)

				writer.writerow([chrm, current, score, int(plot_location)])
				plot_location += (current - previous)
				previous = current

			plot_location += gap

def make_chrom_dct(reader):
	rtn = {}
	for line in reader:

		chrm = line[0]
		pos = line[1]
		count = line[2]

		if chrm not in rtn:
			rtn[chrm] = {}

		rtn[chrm][pos] = count
	return rtn

def get_sorted_keys(dct):
	keys = list(dct.keys())
	keys.sort()
	return keys





get_conservation_score(inf, outf)
			
