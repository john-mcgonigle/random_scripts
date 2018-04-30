#
ssh head-dev

# Set up working enviroment on farm 
source ~/sapientia-web/pipeline/sapientia-task/bin/bootstrap_aws_farm.sh staging

# Change to wirking directory
cd /scratch/personal/johnmcgonigle

# Set up a docker image to run saptientia with
docker run -v /scratch:/scratch -v ~/sapientia-web:/app --rm -t -i 144563655722.dkr.ecr.eu-west-1.amazonaws.com/congenica/pipeline:latest

# Change the dancer environmental variables
export DANCER_APPDIR=/app
export DANCER_ENVIRONMENT=staging


#List potential sapientia tasks
pipeline/sapientia-task/bin/sapientia-task



pipeline/sapientia-task/bin/sapientia-task spreadsheet_to_vcf --chr 1 --pos 2 --ref 3 --alt 4 --keep-columns E,F,I,J,K,L --no-ref-check --spreadsheet /scratch/personal/johnmcgonigle/SOD1_pre_vcf_curated_variant_list.csv > /scratch/personal/johnmcgonigle/SOD1_curated_variant_list.vcf



Example:
#!/bin/bash
WORK_DIR="/scratch/personal/johnmcgonigle"

export LSB_DOCKER_CONTAINER=144563655722.dkr.ecr.eu-west-1.amazonaws.com/congenica/pipeline:latest
export DANCER_ENV=staging
export DANCER_APPDIR=/efs/jmcg/sapientia-web

bsub -o $WORK_DIR/pipeline.out -e $WORK_DIR/pipeline.err \
-q docker sapientia-task create_curated_variant_list --vcf-file /scratch/personal/johnmcgonigle/SOD1_formatted_curated_variant_list.vcf \
--name Biogen_curated_list_formatted \
--user-email john.mcgonigle@congenica.com \
--description "A test SOD1 curated variant list to make sure everything works" \
--pathogenicity_field 'F' 

# current running id 115419




sapientia-task create_curated_variant_list --vcf-file /scratch/personal/jem12/SOD1_formatted_curated_variant_list.vcf \
--name Biogen_final_curated_list \
--user-email john.mcgonigle@congenica.com \
--description "A SOD1 curated variant." \
--pathogenicity_field 'F' 