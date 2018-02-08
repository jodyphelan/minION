export BCFTOOLS_PLUGINS=~/software/bcftools-1.6/plugins/

#mkdir $1
#cd $1
#ln -s $2/*.fastq.gz .
#ls *.fastq.gz | sed 's/.fastq.gz//' > samples.txt
#cat samples.txt | xargs -i -P 4 sh -c "python ~/pathogenseq/scripts/minION_pipeline.py ~/refgenome/MTB-h37rv_asm19595v2-eg18.fa {}.fastq.gz  {} 10"
#cat samples.txt | xargs -i -P 35 sh -c "~/TBProfiler/tb-profiler profile -p {} -t 1 -a {}.bam -m minION"
#cat samples.txt | xargs -i -P 35 sh -c "bgzip {}.vcf"
cat samples.txt | xargs -i -P 35 sh -c "python ../minION/model_time.py {}.fastq.gz  > {}.time_cov.txt"
cat *.time_cov.txt > all_samples.time_cov.txt

python ~/pathogenseq/scripts/merge_vcfs.py  samples.txt ~/refgenome/MTB-h37rv_asm19595v2-eg18.fa all_samples -t 35 --keep_samples samples.txt
~/software/raxml-ng --search --msa all_samples.snps.fa --model GTR+G

bcftools merge all_samples.mix_masked.bcf ~/lgc_dataset/new_pipeline/lgc_illumina.mix_masked.bcf -o minION_illumina_raw.bcf -Ob
python ~/pathogenseq/scripts/bcf2fasta.py minION_illumina_raw.bcf minION_illumina_raw.snps.fa 40
~/software/raxml-ng --search --msa minION_illumina_raw.snps.fa --model GTR+G

python ~/minION/minION/merge_in_illumina.py all_samples.mix_masked.bcf ~/lgc_dataset/new_pipeline/lgc_illumina.mix_masked.bcf minION_illumina.bcf minION_illumina.snps.fa 40
~/software/raxml-ng --search --msa minION_illumina.snps.fa --model GTR+G


grep barcode07_run3 samples.txt  > barcode07.txt
 bcftools view -S barcode07.txt all_samples.mix_masked.bcf -v snps -a  -c 1 -Ob -o barcode07.snps.bcf
bcftools view -S barcode07.txt all_samples.mix_masked.bcf -v indels -a  -c 1 -Ob -o barcode07.indels.bcf

python ../minION/venn.py barcode07.snps.bcf barcode07_run3_batch1,barcode07_run3_batch2,barcode07_run3_batch3,barcode07_run3_batch4 barcode07_snps_venn.pdf
python ../minION/venn.py barcode07.indels.bcf barcode07_run3_batch1,barcode07_run3_batch2,barcode07_run3_batch3,barcode07_run3_batch4 barcode07_indels_venn.pdf


python ~/pathogenseq/scripts/collate_json.py samples.txt  .stats.json > all_samples.stats.txt
Rscript ../minION/variants_vs_dp.R 

Rscript ../minION/cov_vs_time.R 


tar -czvf results.tgz *.pdf *.bestTree all_samples.txt all_samples.dr.itol.txt all_samples.lineage.itol.txt 


