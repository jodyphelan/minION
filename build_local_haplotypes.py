from __future__ import division
import pysam
import sys
from tqdm import tqdm

bamfile = sys.argv[1]
reffile = sys.argv[2]


def build_haplotype(read,start,stop,refseq):
    res = [x for x in read.get_aligned_pairs() if x[1]>=start and x[1]<=stop]
    calls = []
    for q,r in res:
        if q==None:
            calls.append("*")
        elif r==None:
            calls.append("+")
        else:
            calls.append(".")
    return  "".join(calls)

ref = pysam.FastaFile(reffile)
aln  = pysam.AlignmentFile(bamfile,"rb")
chrom = "Chromosome"
ref_seq = ref.fetch(chrom,0,ref.get_reference_length(chrom))
run = 1
nuc = ""
runs = []
print "Counting homopolymeric runs"
for i in tqdm(range(len(ref_seq))):
    new_nuc = ref_seq[i]
    if new_nuc==nuc:
        run+=1
    else:
        if run>1:
            pos = i+1-run
            run_seq = nuc*run
            runs.append((pos,pos+run-1))
        nuc=new_nuc
        run=1
O = open("homopolymer.txt","w")
O.write("pos\trun_len\tseq\tref_frac\n")
for start,end in tqdm(runs):
    run_len = end-start+1
    if run_len<=2: continue
    refseq = ref.fetch(chrom,start,end)
    region = aln.fetch(chrom,start,end)
    haplotypes = []
    for read in region:
        rstart = read.pos
        rend = read.reference_end
        if rstart>start or rend<end: continue
        haplotypes.append(build_haplotype(read,start,end,refseq))
    if len(haplotypes)==0: continue
    num_ref = len([x for x in haplotypes if x=="."*run_len])
    ref_frac = num_ref/len(haplotypes)
    O.write("%s\t%s\t%s\t%s\n" % (start,run_len,refseq,ref_frac))
O.close()
