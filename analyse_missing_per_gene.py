import sys
import pathogenseq as ps

bed_file = sys.argv[1]

bed = ps.load_bed(bed_file,[1,2,3,4],4)
#bed={'pdxH': ('Chromosome', '2934198', '2934872', 'pdxH')}
for l in sys.stdin:
	#1	./.	T/T	T/T	T/T	T/T
	row = l.rstrip().split()
	if "./." in row:
		pos=int(row[0])
		genes = [g for g in bed if int(bed[g][1])<=pos and int(bed[g][2])>=pos]
		gene = genes[0] if len(genes)>0 else "intergenic"
		print "%s\t%s" % ("\t".join(row),gene)

