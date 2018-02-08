from __future__ import division
import sys
from tqdm import tqdm

i = 0
alts = 0
refs = 0
subs = 0
indels = 0
results = []
for l in tqdm(open(sys.argv[1])):
	i+=1
	#Chromosome	  23	  G	   G,G-1C,G+3AAA   0/1:49,1,1
	arr = l.rstrip().split()
	alleles = arr[3].split(",")
	depth = [int(x) for x in arr[4].split(":")[1].split(",")]
	ref_allele_dp = depth[alleles.index(arr[2])] if arr[2] in alleles else 0
	alt_allele_dp = sum(depth)-ref_allele_dp
	indels = [i for i in range(len(alleles)) if "-" in alleles[i] or "+" in alleles[i]]
	
	refs += ref_allele_dp
	alts += alt_allele_dp
	if i==1000:
		results.append(alts/(alts+refs))
		refs=0
		alts=0
		i=0
print "\n".join([str(x) for x in results])
