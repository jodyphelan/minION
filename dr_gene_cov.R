pdf("dr_gene_cov.pdf")
par(mar=c(8,4,4,2)+0.1)
dat<-read.table("drgene_cov.txt",stringsAsFactors = F)
bed<-read.table("drdb.bed",stringsAsFactors = F)
bed$V5[match("Rv0678",bed$V4)]<-"Rv0678"
bed$V5[match("Rv1482c-Rv1483",bed$V4)]<-"inhA_pro"
bed$V5[match("Rv1908c-Rv1909c",bed$V4)]<-"katG_pro"
bed$V5[match("Rv2043c-Rv2044c",bed$V4)]<-"pncA_pro"
bed$V5[match("Rv2416c-Rv2417c",bed$V4)]<-"eis_pro"
bed$V5[match("Rv2427A-Rv2428",bed$V4)]<-"ahpC_pro"
bed$V5[match("Rv3793-Rv3794",bed$V4)]<-"embC_pro"
colnames(dat)<-c("sample","rv","dp")

dat$gene<-bed$V5[match(dat$rv,bed$V4)]
boxplot(dat$dp ~ dat$gene,pch="",ylim=c(0,250),las=2,col="#e2e2e2",boxlwd=1.5,ylab="Coverage")
mtext(text = "Drug resistance genes",side = 1,line = 6)
abline(h=10,col="red",lty=2)
dev.off()
