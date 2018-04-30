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