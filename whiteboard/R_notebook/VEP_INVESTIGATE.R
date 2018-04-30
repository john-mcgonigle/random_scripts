vep_freq<-gsub(";AN", "", unlist(lapply(strsplit(vep$V8, '='), `[[`, 3)))

vep_allele_freq<-c()
for(x in vep_freq)
{
    if (grepl(',', x)){
        tmp<-strsplit(x, ',')
        x <- as.numeric(lapply(tmp, `[[`, 1))
        y <- as.numeric(lapply(tmp, `[[`, 2))
        if (x>y) {
            vep_allele_freq<-c(vep_allele_freq, x)
        }
        else {
            vep_allele_freq<-c(vep_allele_freq, y)
        }

    }
    else{
        vep_allele_freq<-c(vep_allele_freq, as.numeric(x))
    }
}