import sys
import pathogenseq as ps

base_file = sys.argv[1]
merging_file = sys.argv[2]
merged_file = sys.argv[3]
final_fa = sys.argv[4]
threads = sys.argv[5]

base_bcf = ps.bcf(base_file)
base_bcf.merge_in_snps(merging_file,merged_file)
merged_bcf = ps.bcf(merged_file)
merged_bcf.vcf_to_fasta(final_fa,threads)
