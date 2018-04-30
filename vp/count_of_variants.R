rm(list=ls())
library('data.table')
library('foreach')
setwd('/Users/john.mcgonigle/work_dir/data/exac_release_1.0')
list.files()
dat<-fread('gunzip -cq /Users/john.mcgonigle/work_dir/data/exac_release_1.0/ExAC.r1.sites.vep.table.gz')
dat<-data.frame(dat)
exclude_lst<-c('intron_variant', 'upstream_gene_variant', 'downstream_gene_variant')
chrom_len<-read.csv('/Users/john.mcgonigle/work_dir/reference_materials/human_genome/genome_size.csv')
chromsomes<-c('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
              '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'X', 'Y')

head(dat)

freq_filter<-dat$ESP_AF_GLOBAL<0.1
table(freq_filter)
# var_type_filter<-!dat$Consequence%in%exclude_lst
# table(var_type_filter)

# sub<-dat[freq_filter & var_type_filter, ]
sub<-dat[freq_filter, ]
sub<-sub[!is.na(sub[,1]),]

var_count<-function(df, chrm, pos)
{
  foreach(x = unique(df[,chrm]), .combine =rbind) %do%
  {
    print(x)
    tmp<-df[filter_df(df, chrm, x), pos]
    t<-table(tmp)
    cbind(x, names(t), as.vector(t))
  }
}

filter_df<-function(df, column, key)
{
  rtn_filter<-df[,column] %in% key
  c(rtn_filter)
}

count_of_var<-var_count(sub, 1, 2)
count_of_var<-as.data.frame(count_of_var)
names(count_of_var)<-c('Chr', 'Position', 'Count')

head(count_of_var)

write.csv(count_of_var, file='count_of_var.csv', row.names = F)

sum_per_chrom<-function(df, chrm, count)
{
  df[, count]<-as.numeric(df[, count])
  foreach(x = chromsomes, .combine = rbind) %do%
  {
    print(x)
    c(x, sum(df[df[,chrm] %in% x, count]))
  }
}

config_df<-function(df, col_names)
{
  df<-as.data.frame(df)
  row.names(df)<-c()
  names(df)<-col_names
  cbind(df)
}

freq_over_chrom<-sum_per_chrom(count_of_var, 1, 3)
freq_over_chrom<-config_df(freq_over_chrom, c('Chrom', 'Total'))
head(freq_over_chrom)
head(chrom_len)


plot(chrom_len$Chromosome, -log((as.numeric(as.vector(freq_over_chrom$Total))/as.numeric(chrom_len$Size_bp_GRch37.p13)), 10),
     ylim= c(0,5))

#### RUN PYTHON SCRIPT  

dat<-read.csv('/Users/john.mcgonigle/work_dir/data/exac_release_1.0/variant_score_per_locus.csv')
# dat<-fread('/Users/john.mcgonigle/work_dir/data/exac_release_1.0/variant_score_per_locus.csv')
dat<-as.data.frame(dat)
head(dat)

hist(dat$Score, col='blue')
hist(dat$Position, col='red')
hist(as.numeric(as.factor(dat$Chrom)))
unique(dat$Chrom)




conservation_plot<-function(x,y)
{
  png(filename = '/Users/john.mcgonigle/work_dir/data/exac_release_1.0/conservation_plot.png', width = 2600, height = 1400)
  plot(-log(y, 10) ~ x,
       xlab = 'Variants occuring across chromosomes',
       ylab = '-log variant frequency score',
       col = 'blue', 
       pch = 15,
       cex = 0.2)
  dev.off()
}
conservation_plot(dat$Plot_location, dat$Score)
