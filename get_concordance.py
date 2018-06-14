import sys
import pathogenseq as ps
from collections import defaultdict,Counter 
infile = sys.argv[1]

results = defaultdict(int)
for l in ps.cmd_out("bcftools filter -e 'GT=\"het\"' -S . %s | bcftools query -f '[\\t%%TGT]\n'" % infile):
	row = l.rstrip().split()
	gt = Counter([d for d in row if d!="./."])
	print gt
	if sum(gt.values())>1:
		results[len(gt)]+=1
	else:
		results["NA"]+=1

print results		
