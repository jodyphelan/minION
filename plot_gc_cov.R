args = commandArgs(trailingOnly=TRUE)
infile = args[1]
dat<-read.table(infile)
pdf("gc_cov.pdf")
boxplot(dat$V2 ~ dat$V1,col="grey",xlab="GC%",ylab="Coverage",pch=20)
dev.off()
