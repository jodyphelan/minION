grep barcode07_run3 samples.txt  > barcode07.txt
 bcftools view -S barcode07.txt all_samples.mix_masked.bcf -v snps -a  -c 1 -Ob -o barcode07.snps.bcf
bcftools view -S barcode07.txt all_samples.mix_masked.bcf -v indels -a  -c 1 -Ob -o barcode07.indels.bcf

