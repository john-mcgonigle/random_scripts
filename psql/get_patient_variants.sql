#PGPASSWORD=rjyutybrf psql -h 192.168.1.43 -U postgres sapientia_grch38 -f -v v1=10782
#
copy(select variant_id, chr, start, ref_allele, alt_allele, af_kg_max from patient_snv_:v1 join variant using(variant_id)) to stdout with csv header;