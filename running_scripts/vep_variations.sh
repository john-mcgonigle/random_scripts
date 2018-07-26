python /efs/jmcg/scripts/benchmark.py VEP --input-vcf /scratch/personal/jbk/grch38_patient/child1_chr21.vcf \
 --vep-script /usr/local/software/vep/ensembl-vep-release-90.10/vep \
 --vep-cache /scratch/data/VEP_90/ \
 --vep-cache-version '90' \
 --assembly 'GRCh38' \
 --reference-fasta /scratch/data/GRCh38/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa \
 --output-file /scratch/personal/jmcgonigle/random_work/vep/GRCh38_vep90_cache90.vcf \
 --no-progress True \
 --no-stats True \
 --use-given-


 python /efs/jmcg/scripts/benchmark.py VEP --input-vcf /scratch/personal/jbk/grch38_patient/child1_chr21.vcf \
 --vep-script /usr/local/software/vep/ensembl-vep-release-90.10/vep \
 --vep-cache /scratch/data/VEP_90/ \
 --vep-cache-version '90' \
 --assembly 'GRCh38' \
 --reference-fasta /scratch/data/GRCh38/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa \
 --output-file /scratch/personal/jmcgonigle/random_work/vep/GRCh38_vep90_cache90_filtering_at_0.5.vcf \
 --no-progress True \
 --no-stats True \
 --use-given-ref False \
 --check-frequency 0.05 

  python /efs/jmcg/scripts/benchmark.py VEP --input-vcf /scratch/personal/jbk/grch38_patient/child1_chr21.vcf \
 --vep-script /usr/local/software/vep/ensembl-vep-release-90.10/vep \
 --vep-cache /scratch/data/VEP_90/ \
 --vep-cache-version '90' \
 --assembly 'GRCh38' \
 --reference-fasta /scratch/data/GRCh38/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa \
 --output-file /scratch/personal/jmcgonigle/random_work/vep/GRCh38_vep90_cache90_using_given_ref.vcf \
 --no-progress True \
 --no-stats True \
 --use-given-ref True 







python /efs/jmcg/scripts/benchmark.py VEP --input-vcf /efs/jmcg/vep_test.vcf \
 --vep-script /usr/local/software/vep/ensembl-vep-release-90.10/vep \
 --vep-cache /scratch/data/VEP_90/ \
 --vep-cache-version '90' \
 --assembly 'GRCh38' \
 --reference-fasta /scratch/data/GRCh38/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa \
 --output-file /scratch/personal/jmcgonigle/random_work/vep/no_progress_no_stats.vcf \
 --no-progress False \
 --no-stats True \
 --use-given-ref False


python /efs/jmcg/scripts/benchmark.py VEP --input-vcf /efs/jmcg/vep_test.vcf \
 --vep-script /usr/local/software/vep/ensembl-vep-release-90.10/vep \
 --vep-cache /scratch/data/VEP_90/ \
 --vep-cache-version '90' \
 --assembly 'GRCh38' \
 --reference-fasta /scratch/data/GRCh38/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa \
 --output-file /scratch/personal/jmcgonigle/random_work/vep/no_progress_no_stats.vcf \
 --no-progress False \
 --no-stats False \
 --use-given-ref False

python /efs/jmcg/scripts/benchmark.py VEP --input-vcf /efs/jmcg/vep_test.vcf \
 --vep-script /usr/local/software/vep/ensembl-vep-release-90.10/vep \
 --vep-cache /scratch/data/VEP_90/ \
 --vep-cache-version '90' \
 --assembly 'GRCh38' \
 --reference-fasta /scratch/data/GRCh38/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa \
 --output-file /scratch/personal/jmcgonigle/random_work/vep/no_progress_no_stats.vcf \
 --no-progress True \
 --no-stats True \
 --use-given-ref True