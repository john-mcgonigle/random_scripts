BEGIN;

UPDATE ref.gene g
SET (start, "end") =
(SELECT MIN(t.start)
       ,MAX(t."end") 
FROM ref.transcript t
WHERE t.gene_id = g.gene_id
GROUP BY t.gene_id);

COMMIT;
