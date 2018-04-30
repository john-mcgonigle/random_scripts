copy(select * from patient
 join patient_variant using(patient_id)
  join variant using(variant_id)
   where patient_id = :pat_id) to stdout DELIMITER ',' CSV HEADER;

-- In this case :pat_id is going to be passed as an arg e.g.
-- staging -v pat_id=22631 -f get_patient_variants.sql > without_filter.csv