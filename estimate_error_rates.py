from __future__ import division
import sys
import pysam
import subprocess
from tqdm import tqdm
import os.path
import json
import numpy as np

def run_cmd(cmd,verbose=False):
    if verbose==2:
        print "\nRunning command:\n%s" % cmd
        stderr = open("/dev/stderr","w")
    elif verbose==1:
        print "\nRunning command:\n%s" % cmd
        stderr = open("/dev/null","w")
    else:
        stderr = open("/dev/null","w")

    res = subprocess.call(cmd,shell=True,stderr = stderr)
    stderr.close()
    if res!=0:
        print "Command Failed! Please Check!"
	quit()



ref = sys.argv[1]
bam = sys.argv[2]
prefix = bam.split("/")[-1][:-4]
pileup = "%s.pileup" % prefix
outfile = "%s.error_rate.json" % prefix

if not os.path.isfile(pileup):		
	cmd = "htsbox pileup -f %s %s -Q 8 > %s" % (ref,bam,pileup)
	run_cmd(cmd)

tot_ref_dp = 0
tot_alt_dp = 0
cov = []
for l in tqdm(open(pileup)):
	#Chromosome	22813	C	C,A,C-1A,C+1G,C+1T,C+2AA,C+3GAA,C+3TTG	0/1:30,2,1,1,1,1,1,1
	arr = l.rstrip().split()
	alleles = arr[3].split(",")
	dp = [int(x) for x in arr[4].split(":")[1].split(",")]
	if arr[2] in alleles:
		ref_idx = alleles.index(arr[2])
		ref_dp = dp[ref_idx]
	else:	
		ref_dp = 0
	alt_dp = sum(dp)-ref_dp
	tot_ref_dp += ref_dp	
	tot_alt_dp += alt_dp
	cov.append(sum(dp))

error_rate = {"coverage":np.mean(cov), "tot_ref_bases":tot_ref_dp,"tot_alt_bases":tot_alt_dp,"error_rate":tot_alt_dp/(tot_ref_dp+tot_alt_dp)}

for x in error_rate:
	print "%s\t%s\t%s" % (prefix,x,error_rate[x])

json.dump(error_rate,open(outfile,"w"))
