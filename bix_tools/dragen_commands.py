
dragen -f -r /staging/human/reference/GRCh38 -b /staging/jem/merged_trio/mum.bam --generate-md-tags true \
--enable-duplicate-marking true --enable-variant-caller true --enable-map-align-output true \
--vc-reference /staging/human/reference/hg19/GRCh38.fa --output-directory /staging/jem/merged_trio/output/  \
--vc-emit-ref-confidence=GVCF --vc-max-alternate-alleles=6 --vc-sample-name EGAN00001088114 --enable-bam-indexing true \
--output-file-prefix NA12878 --vc-sex=FEMALE

dragen -r /staging/human/reference/GRCh38/ -b /staging/jem/merged_trio/mum.bam \
--generate-md-tags true --enable-duplicate-marking true \
--enable-variant-caller true --enable-map-align-output true \
--vc-reference /staging/human/reference/GRCh38/Homo_sapiens_assembly38.fasta \
--output-directory /staging/jem/merged_trio/output/ \
--vc-sample-name EGAN00001088114 --vc-emit-ref-confidence=GVCF \
--vc-max-alternate-alleles=6 --enable-bam-indexing true \
--output-file-prefix MUM --vc-sex=FEMALE

dragen -r /staging/human/reference/GRCh38/ \
--enable-joint-genotyping true \
--variant-list=/staging/jem/merged_trio/output/gvcfs_files.txt \
--output-directory /staging/jem/merged_trio/output/ \
--output-file-prefix JOINT_CALLED 


gatk HaplotypeCaller \
-R /scratch/data/GRCh38/GATK_bundle/Homo_sapiens_assembly38.fasta \
-I /scratch/projects/trio_calling/trio_calling/data/MUM.bam \
-O /scratch/projects/trio_calling/hapcaller_test.vcf 