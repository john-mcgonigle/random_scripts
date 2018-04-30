samtools view -H test.bam | grep '^@RG' | sed "s/.*SM:\([^\t]*\).*/\1/g" | uniq
tail -n 1 /scratch/logs/docker_runner.log