copy(select "gene_id"
, "name"
, "start"
, "end"
, "default_transcript_id"
, "ensembl_id"
 from gene) to stdout DELIMITER ',' CSV HEADER;

