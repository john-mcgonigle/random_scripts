dat<-read.csv('~/work_dir/interview_data.csv')
head(dat)
table(dat$pathogenicity)
path_rank<-rep(NA, nrow(dat))
path_rank[dat$pathogenicity=='Clearly not pathogenic']<-4
path_rank[dat$pathogenicity=='Unlikely to be pathogenic']<-3
path_rank[dat$pathogenicity=='Likely to be pathogenic']<-2
path_rank[dat$pathogenicity=='Clearly pathogenic']<-1
table(path_rank)
dat<-cbind(dat,path_rank)
write.csv(dat, file='~/work_dir/interview_challenge.csv', row.names = F)

dat<-read.csv('~/work_dir/interview_challenge.csv')
deduped.data<-unique(dat)
dat<-deduped.data
dat$global_rank<-c(1:nrow(dat))
head(dat)
write.csv(dat, file='~/work_dir/interview_challenge.csv', row.names = F)
dat$variant_id<-c(1:nrow(dat))
dat$gene_id<-c(1:nrow(dat))+floor(runif(nrow(dat), 0, 1000000))
table(dat$gene)
head(dat)
ndat<-dat[order(rnorm(nrow(dat))),1:ncol(dat)-1]
ranks<-ndat$path_rank
ndat<-ndat[,1:15]
###########
four_range<-c(rep(4, 14), rep(3, 4), rep(2, 2), rep(1,1), rep(5,1))
three_range<-c(rep(4, 4), rep(3, 19), rep(2, 4), rep(1,2), rep(5,1))
two_range<-c(rep(4, 2), rep(3, 4), rep(2, 20), rep(1,4), rep(5,1))
one_range<-c(rep(4, 1), rep(3, 2), rep(2, 4), rep(1,22), rep(5,1))
na_range<-c(rep(4, 3), rep(3, 2), rep(2, 2), rep(1,1), rep(5,22))

############
bias_maker<-function(column, values, x)
{
  filt<-column==x
  replace_values<-sample(values, table(filt)[2], replace=T)
  column[which(filt)]<-replace_values
  c(column)
}

variation_adder<-function(column, values)
{
  filt<-is.na(column)
  replace_values<-sample(values, table(filt)[2], replace=T)
  column[which(filt)]<-replace_values
  c(column)
}

humanizer<-function(column)
{
  tmp<-bias_maker(column, four_range, 4)
  print(length(tmp))
  tmp<-bias_maker(tmp, three_range, 3)
  print(length(tmp))
  tmp<-bias_maker(tmp, two_range, 2)
  print(length(tmp))
  tmp<-bias_maker(tmp, one_range, 1)
  print(length(tmp))
  tmp<-variation_adder(tmp, na_range)
  print(length(tmp))
  tmp[tmp==5]<-NA
  c(tmp)
}

Doctor_1<-humanizer(ranks)
Doctor_2<-humanizer(ranks)
Doctor_3<-humanizer(ranks)
Doctor_4<-humanizer(ranks)
Doctor_5<-humanizer(ranks)
Doctor_6<-humanizer(ranks)
Doctor_7<-humanizer(ranks)
Doctor_8<-humanizer(ranks)
Doctor_9<-humanizer(ranks)
Doctor_10<-humanizer(ranks)

candidate<-cbind(ndat, Doctor_1, Doctor_2, Doctor_3, Doctor_4, Doctor_5, Doctor_6, Doctor_7, Doctor_8, Doctor_9, Doctor_10)
head(candidate)

write.csv(candidate, file = '~/work_dir/interview_challenge_candidate.csv', row.names = F)


