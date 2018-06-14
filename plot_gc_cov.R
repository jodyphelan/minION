pdf("gc_skew.pdf")

dat<-read.table("gc_skew.txt",stringsAsFactors = F)
colnames(dat)<-c("sample","gc","dp")
bp<-boxplot(dat$dp ~ dat$gc,pch="",ylim=c(0,250),las=2,col="#e2e2e2",boxlwd=1.5,xlab="GC%",ylab="Coverage")
abline(h=10,col="blue",lty=2)
cut<-which(bp$stats[3,]<10)[1]-0.5
abline(v=cut,col="red",lty=2)

dev.off()
