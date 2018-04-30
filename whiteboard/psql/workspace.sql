select * from transcript
 join transcript_to_exon using(transcript_id)
 join exon using(exon_id)
 where name='NM_000044';