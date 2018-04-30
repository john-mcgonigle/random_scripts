import subprocess
# path = 'http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/GRCh38_positions/ALL.chrIDX_GRCh38.genotypes.20170504.vcf.gz'
# path = 'http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chrIDX.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz'
# chrms = [str(i) for i in range(2,23)]
# chrms += ['http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chrMT.phase3_callmom-v0_4.20130502.genotypes.vcf.gz',
# 		  'http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz',
# 		  'http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chrY.phase3_integrated_v2a.20130502.genotypes.vcf.gz']
# chrms += ['X', 'Y']
path = 'ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/related_samples_vcf/ALL.chrIDX.phase3_shapeit2_mvncall_integrated_v5_related_samples.20130502.genotypes.vcf.gz'
chrms = [str(i) for i in range(2,23)]
chrms += ['ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/related_samples_vcf/ALL.chrY.phase3_integrated_v2a_related_samples.20130502.genotypes.vcf.gz']

def wget_many(path, idxs):
	processes = []
	for i in idxs:
		wget_path = path.replace('IDX', i)
		# print(wget_path)
		command = ['wget', '-bc', wget_path]
		handle = subprocess.Popen(command)
		processes.append(handle)

	for handle in processes:
		handle.wait()

wget_many(path, chrms)