library(scales)
dat<-read.table("all_samples.stats.txt",header = T)


batches<-substr(dat$sample,16,21)
batches.uniq<-unique(batches)
cols.uniq<-rainbow(4)
cols<-cols.uniq[match(batches,batches.uniq)]

corr.func<-function(x,y,...){
 # par(usr = c(0, 1, 0, 1))
  print(par("usr"))
  p<-par("usr")
  xrange<-p[2]-p[1]
  yrange<-p[4]-p[3]
  x1<-p[1]+xrange*0.1
  x2<-p[1]+2*xrange*0.1
  xmid<-(x1+x2)/2
  y1<-p[3]+yrange*0.1
  y2<-p[3]+2*yrange*0.1
  ymid<-(y1+y2)/2
  text((p[1]+p[2])/2,(p[3]+p[4])/2,signif(cor(x,y),digits=2),cex=1.3)

  b<-boxplot(y, plot = FALSE)
  rect(x1,b$stats[2,1],x2,b$stats[4,1],col="grey")
  segments(xmid,b$stats[2,1],xmid,b$stats[1,1])
  segments(xmid,b$stats[4,1],xmid,b$stats[5,1])
  segments(x1,b$stats[3,1],x2,b$stats[3,1])
  
  b<-boxplot(x, plot = FALSE)
  rect(b$stats[2,1],y1,b$stats[4,1],y2,col="grey")
  segments(b$stats[2,1],ymid,b$stats[1,1],ymid)
  segments(b$stats[4,1],ymid,b$stats[5,1],ymid)
  segments(b$stats[3,1],y1,b$stats[3,1],y2)
}
dens.func<-function(x,...){
  p<-par("usr")
  p[3]<-0
  p[4]<-1.5
  par(usr = p) 
  d<-density(x,from=min(x),to=max(x))
  y<-c(0,scale(d$y,scale = max(d$y),center = F),0)
  x<-c(d$x[1],d$x,d$x[length(d$x)])
  points(x,y,type="l",lwd=2)
  polygon(x,y,col="light blue")
}
pdf("stats.pdf")
pairs(
      dat[,c("med_dp","median_read_len","pct_reads_mapped","read_num")],
      labels=c("Median Depth","Med Read Len","% Reads Mapped","Read Num"),
      pch=20,col=alpha(cols,0.5),cex=1.5,cex.labels = 1.2,upper.panel = corr.func,diag.panel = dens.func
)
dev.off()

pdf("cov_per_batch.pdf")
par(mar=c(4,4,2,4)+0.1)
x<-(dat$median_read_len*dat$read_num)/1e9
par(lwd=2)
barplot(tapply(x,batches,sum),las=1,ylab="Data (Gb)",lwd=2,col=alpha(cols.uniq,0.5))
par(lwd=1)
abline(h=0,lwd=2)
z<-((tapply(x,substr(dat$sample,16,21),sum)*1e9)/7)/4.4e6
sf<-z[1]/tapply(x,substr(dat$sample,16,21),sum)[1]
labs<-seq(0,120,20)
axis(4,at=scale(labs,scale=sf,center=F),labels =labs,lwd=2 )
mtext("Coverage per Mtb sample",4,at=2,line = 3)
dev.off()
