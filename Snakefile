

rule zero:
	input:
		"zapusk.txt"
	output:
		"Horde.vcf"
	shell:
		"/usr/local/bin/bcftools merge -m all -i AC:sum,AN:sum --force-samples -l {input} -o Horde.vcf"

	
rule first:
	input:
		rules.zero.output
	output:
		"ref_0.vcf.gz"
		
	shell:
		"/usr/local/bin/bcftools +missing2ref {input} | /usr/local/bin/bcftools +fill-tags | bgzip -c  > {output[0]} "


rule second:
	input: 
		rules.first.output		
	output:
		"minDP_10_minGQ_15.vcf"
	shell: 
		"/usr/local/bin/bcftools filter --output minDP_10_minGQ_15.vcf -i 'MIN(DP)>10 && MIN(GQ)>15'  {input}"


rule third:
	input:
		rules.second.output
		
	output:
		"Vivod.tab.gz"		
	shell:
		"/usr/local/bin/bcftools query -f'%CHROM\t%POS\t%REF\t%ALT\t%AN\t%AC\t%AC_Hom\t%AC_Hemi\t%AC_Het\n' {input[0]} | sed 's/chr//g' | bgzip -c > {output} && tabix -p vcf {output}"


