

rule check_gz:
	input:
		"zapusk.txt"
	output:
		temp("zapusk2.txt")
	shell:
		"python variantics.py check_gz --vcf {input}"
		

rule merge:
	input:
		rules.check_gz.output
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
		"/usr/local/bin/bcftools +setGT {input} -- -t q -i 'DP<10 || GQ<15' -n . > {output}"


rule final:
	input:
		rules.filter.output
		
	output:
		"1variant_statistics.tab.gz"		
	shell:
		"/usr/local/bin/bcftools query -f'%CHROM\t%POS\t%REF\t%ALT\t%AN\t%AC\t%AC_Hom\t%AC_Hemi\t%AC_Het\n' {input[0]} | sed 's/chr//g' | bgzip -c > {output} && tabix -p vcf {output}"

rule remove:
	input:
		rules.final.output
	output:
		"variant_statistics.tab.gz"
	shell:
		"python variantics.py remove --vcf {input}"
