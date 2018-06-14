import sys
import pathogenseq as ps

infile = sys.argv[1]
bcf = ps.bcf(infile)
stats = bcf.load_stats()
#stats = {'PSC': {'barcode07_run1_batch1': {'nHets': 798,'nNonRefHom': 38,'nRefHom': 276198}}}
if len(sys.argv)>2:
	genome_len = sum([len(x) for x in ps.fasta(sys.argv[2]).fa_dict.values()])
if len(sys.argv)>2:
	print "sample\tnRefHom\tnNonRefHom\tnHets\tnMissing"
else:
	print "sample\tnRefHom\tnNonRefHom\tnHets"
for sample in stats["PSC"]:
	s = stats["PSC"][sample]
	if len(sys.argv)>2:
		tot_sum = s["nRefHom"]+s["nNonRefHom"]+s["nHets"]
		print "%s\t%s\t%s\t%s\t%s" % (sample,s["nRefHom"],s["nNonRefHom"],s["nHets"],genome_len-tot_sum)
	else:
		print "%s\t%s\t%s\t%s" % (sample,s["nRefHom"],s["nNonRefHom"],s["nHets"])
