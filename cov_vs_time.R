library(scales)
library(drc)
library(data.table)
dat<-as.data.frame(fread("all_samples.time_cov.txt"))
colnames(dat)<-c("sample","time","read_num","bases","cov")
batches<-c("batch1","batch2","batch3","batch4")
cols<-rainbow(4)

xlims<-c(0,max(dat$time))
ylims<-c(0,max(dat$cov))
pdf("cov_vs_time.pdf")
plot(1,1,type="n",xlim=xlims,ylim=ylims,xlab="Time (Hours)",ylab="Coverage")
batch_type<-c()
km<-c()
for (x in unique(dat$sample)){
  print(x)
  tmp<-subset(dat,sample==x)
  b<-substr(x,16,21)
  col<-cols[match(b,batches)]
  if (sum(tmp$time)==0){
    next
  }
  points(tmp$cov ~ tmp$time,type="l",col=col)
  model<-drm(tmp$cov ~ tmp$time, fct = MM.2())
  batch_type<-c(batch_type,b)
  km<-c(km,coef(model)[2])
}
legend("bottomright",legend=batches,fill=rainbow(4))
dev.off()

pdf("flow_cell_half_life.pdf")
boxplot(km ~ batch_type,ylab="Flow cell half-life",col=alpha(rainbow(4),0.5))
dev.off()

