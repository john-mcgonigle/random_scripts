setwd('/Users/john.mcgonigle/scripts/persistent_id')
dat<-read.csv('vcf_comparison_summary.vcf')
head(dat)
nrow(dat)
png(file='Initial_analysis_histogram_persitentID.png', width = 1000, height = 600)
par(mar=c(5,5,1,1))
hist(dat$Proportion, 30, 
     col='blue',
     xlab = 'Proportion of sites shared',
     ylab = 'Frequency',
     family='Times',
     cex.lab= 2,
     cex.axis = 1.5,
     main = '',
     xlim = c(0.40,1))
dev.off()

lamda<-(dat$Proportion*100)/length(dat$Proportion)

dat[dat$Proportion>0.9,]

(a + b + 1) * (a + b) // 2 + b

p<-median(dat$Proportion)
0.95-p/  sqrt(((p*(1-p))/length(dat$Proportion)))
pnorm(-9.21, mean = 0.5)

0.95-0.49/sd(dat$Proportion)
pnorm(-9.38)

x<-c(rep(1, 60), rep(2, 20), rep(3, 10), rep(4, 5), rep(5, 3), rep(6, 3), rep(7, 2), rep(8,2), rep(9,2), rep(10,1))
hist(x,100)