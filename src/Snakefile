configfile: "config.json"
workdir: config["results_folder"]
var = config["var"]
out = config["results_folder"]
rule check_gz:
	input:
		config["input_data"],
		
	output: 
		config["Upgrade_input_data"]
	shell:
		"python {var} check_gz --data {out}/{input}"

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
		temp("filtered_minDP_10_minGQ_15.vcf")
	shell: 
		"/usr/local/bin/bcftools +setGT {input} -- -t q -i 'DP<4' -n . > {output}"

# rule hist

rule final:
	input:
		rules.filter.output
	output:
		"variant_statistics.tab.gz"
	shell:
		"/usr/local/bin/bcftools query -f'%CHROM\t%POS\t%REF\t%ALT\t%AN\t%AC\t%AC_Hom\t%AC_Hemi\t%AC_Het\n' {input[0]} | sed 's/chr//g' | bgzip -c > {output} && tabix -p vcf {output}"


