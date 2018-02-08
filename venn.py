import sys
import pathogenseq as ps

infile = sys.argv[1]
samples =sys.argv[2]
outfile = sys.argv[3]
x = ps.bcf(infile)
x.get_venn_diagram_data(samples=samples,outfile=outfile)
