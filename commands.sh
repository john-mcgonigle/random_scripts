# Commands
 scp -i .ssh/colt.pem [INSERT_FILE_HERE]  colt@80.169.12.164:{PATH_TO_GO_TO}

 scp -i ~/.ssh/colt.pem colt@80.169.12.164:~/shoulders.pem.nc .

 scp -i ~/.ssh/colt.pem /mnt/c/work_dir/sapientia-web/pipeline/ngps/create_patient_data/genotype_methods/*.py colt@80.169.12.164:/scratch/data/con-jem/scripts/NGPS/genotype_methods/

 scp -i ~/.ssh/colt.pem colt@80.169.12.164:/scratch/data/con-jem/dbSNP_SOD1.vcf .

 rename 's/string_to_replace/replace_with/g' *

 rename 's/phase_cohort/phase3_cohort/g' *

 rename 's/HG00240a_HG00240b/singleton_person2_/g' *

rename 's/b.txt/b_infected.txt/g' *


# This command replaces any empty fields with '.'
awk 'BEGIN { FS = OFS = "\t" } { for(i=1; i<=NF; i++) if($i ~ /^ *$/) $i = "." }; 1' SOD1_curated_variant_list.vcf


tail --line +7 SOD1_curated_variant_list.vcf | awk 'BEGIN { FS = OFS = "\t" } { for(i=1; i<=NF; i++) if($i ~ /=/) \
gsub("%20",  " "); gsub("pathogenic ",  "pathogenic") }; 1' > tmp.txt

head -n 6 SOD1_curated_variant_list.vcf > header.txt

cat header.txt tmp.txt > SOD1_formatted_curated_variant_list.vcf

# Selects certain columns and then replaces :. with nothing, 1/1 with 1, 0/1 with 0, 0/2 with 2 and 2/1 with 3
cut -f1,2,4,5,10 $1 | sed "s/:.*$//g"  | sed "s/1\/1/1/g" | sed "s/0\/1/0/g" | sed "s/0\/2/2/g"  | sed "s/2\/1/3/g"  | grep -v "," > $2/${a}

sed "s/chrX/X/g"

rename 's/ /_/g' *
rename 's/*/chr/g' *

sed -e "s/0|1/1|0/g;n" tmp

sed -e "s/1\/0/1|0/g" | sed "s/0\/0/0|0/g" | sed "s/1\/1/1|1/g"| sed "s/0\/1/0|1/g" | sed "s/2\/1/2|1/g" | sed "s/1\/2/1|2/g" | sed "s/3\/1/3|1/g" | sed "s/2\/3/2|3/g" | sed "s/1\/3/1|3/g" > tmp


grep '^X' giab_formatted_dad.vcf | sed "s/1|1/0/g" | | sed "s/1|0/1/g"| sed "s/0|1/1/g" | sed "s/1|2/1/g" > X

cut -f 10 X | cut -d : -f 1 | grep -v '#' | sort | uniq -c

grep '^X' giab_formatted_dad.vcf | sed "s/1\/1/1/g" | sed "s/0\/1/1/g" | sed "s/1\/0/1/g" | sed "s/2\/1/2/g" | sed "s/1\/2/2/g" > X

#Will echo the command so you don't need to worry about it
for i in ../*.vcf; do filename=$(basename $i); c=${filename%.phase*}; ss=${c##*.}; echo  time bcftools +split $i -Oz -o $ss/ -i'GT="alt"'; done

for i in ../*.vcf; do filename=$(basename $i); c=${filename%.phase*}; ss=${c##*.}; echo "Processing $i"; time bcftools +split $i -Oz -o $ss/ -i'GT="alt"'; done