from __future__ import division
import sys
import gzip
import datetime
import re

if len(sys.argv)!=2:
	print "python model_time.py <fastq>"
	quit()

fastq = sys.argv[1]
prefix = fastq.split("/")[-1].split(".fastq")[0]
IN = gzip.open(fastq)
times = []
i=0
while True:
	name = IN.readline()
	if name=="": break
	seq = IN.readline()
	IN.readline()
	IN.readline()

	#start_time=2017-10-20T18:49:32Z
	date = re.search("start_time=(\S+)",name).group(1)
	y = int(date[:4])
	m = int(date[5:7])
	d = int(date[8:10])
	h = int(date[11:13])
	mi = int(date[14:16])
	s = int(date[17:19])
	start = datetime.datetime(y,m,d,h,mi,s)
	times.append((start,len(seq)))

times.sort(key=lambda x:x[0])
start = times[0][0]
i=0
num_bases = 0
for d,seqlen in times:
	i+=1
	num_bases+=seqlen
	td = d-start
	sd = (td.days*60*60*24)+td.seconds
	cov = num_bases/4.4e6
	print "%s\t%s\t%s\t%s\t%s" % (prefix,sd/3600,i,num_bases,cov)

