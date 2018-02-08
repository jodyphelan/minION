from __future__ import division
import sys
import subprocess
import os.path

bam = sys.argv[1]
ref = sys.argv[2]
allele_frac = float(sys.argv[3])
min_dp = int(sys.argv[4])
prefix = bam.split("/")[-1].split(".bam")[0]

temp = "%s.pileup" % prefix

if not os.path.isfile(temp):
	subprocess.call("htsbox pileup -f %s %s > %s" % (ref,bam,temp),shell=True)

for l in open(temp):
	arr = l.rstrip().split()
	alleles = arr[3].split(",")
	depth = [int(x) for x in arr[4].split(":")[1].split(",")]
	tot_dp = sum(depth)
	ref = arr[2]
	pos= arr[1]
	max_allele_dp = max(depth)
	max_allele = "".join([alleles[i] for i in range(len(alleles)) if depth[i]==max_allele_dp])
	max_allele_frac = max_allele_dp/tot_dp
	adjusted_allele_frac = max_allele_dp/(max_allele_dp+sorted(depth)[-2]) if len(depth)>1 else max_allele_frac

	ref_dp = depth[alleles.index(ref)] if ref in alleles else 0
	ref_frac = ref_dp/tot_dp
	adjusted_ref_frac = ref_dp/(max_allele_dp+sorted(depth)[-2]) if len(depth)>1 else max_allele_frac
	if max_allele_frac<allele_frac: continue
	if tot_dp<min_dp: continue
	if max_allele!=ref:
		print l

