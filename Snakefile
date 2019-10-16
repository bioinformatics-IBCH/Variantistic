
rule check_gz:
	input:
		"zapusk.txt"
	output:
		temp("zapusk2.txt")
	script:
		"WriteListVcf.py"
		

rule merge:
	input:
		"zapusk2.txt"
	output:
		temp("Horde.vcf")
	shell:
		"/usr/local/bin/bcftools merge -m all -i AC:sum,AN:sum --force-samples -l {input} -o Horde.vcf"

	
rule start_extract:
	input:
		rules.merge.output
	output:
		temp("ref_0.vcf.gz")
		
	shell:
		"/usr/local/bin/bcftools +missing2ref {input} | /usr/local/bin/bcftools +fill-tags | bgzip -c  > {output[0]} "


rule filter:
	input: 
		rules.start_extract.output		
	output:
		"minDP_10_minGQ_15.vcf"
	shell: 
		"/usr/local/bin/bcftools filter --output minDP_10_minGQ_15.vcf -i 'MIN(DP)>10 && MIN(GQ)>15'  {input}"


rule final:
	input:
		rules.filter.output
		
	output:
		"variant_statistics.tab.gz"		
	shell:
		"/usr/local/bin/bcftools query -f'%CHROM\t%POS\t%REF\t%ALT\t%AN\t%AC\t%AC_Hom\t%AC_Hemi\t%AC_Het\n' {input[0]} | sed 's/chr//g' | bgzip -c > {output} && tabix -p vcf {output}"


