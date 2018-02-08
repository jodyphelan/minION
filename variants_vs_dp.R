dat<-read.table("all_samples.stats.txt",header = T,stringsAsFactors = F)
h37rv<-dat[substr(dat$sample,0,14)=="barcode07_run3",]
pdf("variant_vs_dp.pdf")
plot(dat$hom_variants ~ dat$med_dp,xlab="Median depth of coverage",ylab="Number of variants",pch=20)
dev.off()
