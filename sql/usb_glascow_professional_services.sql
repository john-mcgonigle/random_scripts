COPY(SELECT core.patient.patient_id as sapientia_patient_id
    , ref.variant_transcript.variant_id as sapientia_variant_id
    , gene.name
    , ref.variant."chr"
    , ref.variant."start"
    , ref.variant.ref_allele
    , ref.variant.alt_allele
    , ref.variant.af_max
    , ref.variant.hgmd_id
    , ref.variant.rs_id
    , ref.variant_transcript.hgvs_c
    , ref.variant_transcript.hgvs_p
    , ref.variant_transcript.codons
    , ref.variant_transcript.amino_acid
    , ref.variant_transcript.protein_position
    , ref.variant_transcript.vep_consequence
    , ref.variant_transcript.polyphen_prediction
    , ref.variant_transcript.polyphen_score
    , ref.variant_transcript.sift_prediction
    , ref.variant_transcript.sift_score
    , ref.variant_transcript.domains
    , ref.variant_transcript.uniprot_acc_id
    , ref.variant.af_max as Max_Allele_Frequency
    , core.patient_snv.genotype as Zygosity
    , core.patient_snv.inheritance as Inheritance
    FROM core.patient
    JOIN core.patient_variant USING (patient_id)
    JOIN core.patient_snv USING (patient_variant_id)
    JOIN ref.variant_transcript ON patient_variant.variant_id=ref.variant_transcript.variant_id
    JOIN ref.variant ON patient_variant.variant_id=ref.variant.variant_id
    JOIN ref.variant_gene ON patient_variant.variant_id=ref.variant_gene.variant_id
    JOIN ref.gene USING (gene_id)
    WHERE core.patient.project_id = 466
    AND ref.variant.af_max < 0.1)
TO STDOUT WITH CSV HEADER;

-- AND '|PPP3CA|ABAT|SLC6A5|MEF2C|BSN|ADCY8|MTHFR|PCSK4|DSCAML1|' LIKE '%|' || ref.gene.name || '|%'