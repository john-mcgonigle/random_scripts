copy(select transcript.gene_id
    , transcript.transcript_id
    , exon.exon_id
    , exon.start
    , exon.end
    , transcript.name
from exon
join transcript_to_exon using(exon_id)
join transcript using (transcript_id)
where transcript.name like '%ENS%') to stdout DELIMITER ',' CSV HEADER;


select transcript.gene_id
    , transcript.transcript_id
    , exon.exon_id
    , exon.start
    , exon.end
    , transcript.name
from exon
join transcript_to_exon using(exon_id)
join transcript using (transcript_id)
where transcript.name like '%ENS%';