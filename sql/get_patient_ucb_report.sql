CREATE OR REPLACE FUNCTION cache_2.get_PS11_report(_patient_ids integer[])
RETURNS TABLE(
    patient_variant_id           bigint
   ,patient_id                   integer
   ,variant_id                   bigint
   ,chr                          ref.chromosome
   ,start                        bigint
   ,ref_allele                   ref.sequence
   ,alt_allele                   ref.sequence
   ,genotype                     core.variant_genotype
   ,hgmd_id                      character varying
   ,rs_id                        character varying
   ,hgvs_c                       character varying
   ,hgvs_p                       character varying
   ,codons                   character varying
   ,amino_acid                   character varying
   ,protein_position             character varying
   ,polyphen_prediction          character varying
   ,polyphen_score               double precision
   ,sift_prediction              character varying
   ,sift_score                   double precision
   ,domains                      text
   ,uniprot_acc_id               character varying
   ,inheritance                  core.variant_inheritance
   ,filter                       character varying
   ,vep_consequences             ref.vep_consequence_ensembl_81[]
   ,gene_name                    character varying
   ,af_max                       double precision)
SECURITY DEFINER AS $$
---------------------------------------------------------------------------------
--      Function    : get_PS11_report
--      Description : returns detailed list of snvs for the patient ids provided
---------------------------------------------------------------------------------
DECLARE
  _exists_patient_ids integer[];
  _patient_id integer;
  v_sql_base_query text :=
  'SELECT
    cache.patient_variant_id
   ,cache.patient_id as sapientia_patient_id
   ,cache.variant_id as sapientia_variant_id
   ,cache.chr
   ,cache.start
   ,cache.ref_allele
   ,cache.alt_allele
   ,cache.genotype
   ,cache.hgmd_id
   ,cache.rs_id
   ,cache.hgvs_c
   ,cache.hgvs_p
   ,cache.codons
   ,cache.amino_acid
   ,cache.protein_position
   ,cache.polyphen_prediction
   ,cache.polyphen_score
   ,cache.sift_prediction
   ,cache.sift_score
   ,cache.domains
   ,cache.uniprot_acc_id
   ,cache.inheritance
   ,cache.filter
   ,cache.vep_consequences
   ,cache.gene_name
   ,cache.af_max
FROM cache_2.table_of_patient_snv_to_gene_transcript_';
  v_sql_join_predicate text := ' AS cache
JOIN ref.gene AS gene USING (gene_id)
JOIN ref.variant AS variant USING (variant_id) ';
    v_sql_query_predicate text := ' WHERE af_max < 0.1'
    AND '|PPP3CA|ABAT|SLC6A5|MEF2C|BSN|ADCY8|MTHFR|PCSK4|DSCAML1|' LIKE '%|' || gene_name || '|%';
    -- to add filter conditions replace variable e.g.
    --  v_sql_query_predicate text := ' WHERE inheritance = ''de-novo''::variant_inheritance  GROUP BY patient_id, gene_id';
    v_sql_full_query text;
BEGIN
    SELECT cache_2.get_existing_patients_with_snv_caches(_patient_ids) INTO _exists_patient_ids;
    v_sql_full_query := v_sql_base_query||_exists_patient_ids[1]::varchar||v_sql_join_predicate||v_sql_query_predicate;
    FOR _patient_id IN 2 .. array_upper(_exists_patient_ids,1) LOOP
        v_sql_full_query := v_sql_full_query||' UNION ALL ';
        v_sql_full_query := v_sql_full_query||v_sql_base_query||_exists_patient_ids[_patient_id]::varchar||v_sql_join_predicate||v_sql_query_predicate;
    END LOOP;
    -- to debug return RAISE INFO '%', v_sql_full_query;
    RETURN QUERY
    EXECUTE v_sql_full_query;
END;