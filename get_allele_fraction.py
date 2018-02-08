from __future__ import division
import sys
import subprocess
import os.path

bam = sys.argv[1]
ref = sys.argv[2]
allele_frac = [x/50 for x in range(50)] if sys.argv[3]=="all" else sorted([float(x) for x in sys.argv[3].split(",")])
prefix = bam.split("/")[-1].split(".bam")[0]
temp = "%s.pileup" % prefix

if not os.path.isfile(temp):
	subprocess.call("htsbox pileup -f %s %s > %s" % (ref,bam,temp),shell=True)

O = open("%s.depth" % prefix,"w")
fp = {f:0 for f in allele_frac}
fp_snp = {f:0 for f in allele_frac}
fp_indel = {f:0 for f in allele_frac}
tp = {f:0 for f in allele_frac}
miss = {f:0 for f in allele_frac}
tot_bases = 0
tb = 0
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
	if max_allele==ref:
		tb+=1
#	print "%s\t%s\t%s" % (pos,ref_frac,max_allele==ref)
	for f in allele_frac:
		if max_allele_frac>f and max_allele==ref:
			tp[f] += 1
		elif max_allele_frac>f and max_allele!=ref:
			fp[f] += 1
			if len(max_allele)>1:
				fp_indel[f]+=1
			else:
				fp_snp[f]+=1	
		elif max_allele_frac<f:
			miss[f]+=1
	tot_bases+=1
	O.write("%s\t%s\t%s\t%s\n" % (pos,ref_dp,ref_frac,tot_dp))
O.close()

S = open("%s.call_rate.txt" % prefix,"w")
S.write("sample\tcutoff\tcall_rate\tmiss_rate\tfp_snps\tfp_indels\n")
for f in allele_frac:
	tp_rate = (tp[f]/(tp[f]+fp[f]))
	miss_rate = miss[f]/tot_bases
	S.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (prefix,f,tp_rate,miss_rate,fp_snp[f],fp_indel[f]))
S.close()
