#!/bin/bash
WORK_DIR=/scratch/personal/jmcgonigle/test_pipelines/convert_ir_tiering_to_vcf
BASE_DIR=/scratch/personal/jmcgonigle

export LSB_DOCKER_CONTAINER=144563655722.dkr.ecr.eu-west-1.amazonaws.com/congenica/pipeline:latest
export DANCER_ENVIRONMENT=staging
export DANCER_APPDIR=/scratch/personal/jmcgonigle/sapientia-web
export LUNAR_JOB_ID=overninethousand

if [ ! -d $WORK_DIR ]; then
    mkdir $WORK_DIR;
fi

bsub -q normal -o $WORK_DIR/pipeline.out -e $WORK_DIR/pipeline.err \
   python $BASE_DIR/sapientia-web/pipeline/ruffus/convert_tiering_file.py \
   --pipeline-env docker_farm --jobs 24 --verbose 3 \
   --work-dir $WORK_DIR \
   --tiering-file $WORK_DIR/ir.tiering \
   --assembly 'GRCh37'\
   --dry-run
