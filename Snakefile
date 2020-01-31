configfile: "config.json"
workdir: config["results_folder"]
var = config["var"]
out = config["results_folder"]

rule check_files_are_gzipped:
    input:
         config["input_data"],
    output:
          config["upgrade_input_data"]
    shell:
         "variantics check_gz --data {out}/{input}"

rule merge:
    input:
         rules.check_files_are_gzipped.output
    output:
          temp("Horde.vcf")
    shell:
         "bcftools merge -m all -i AC:sum,AN:sum --force-samples -l {input} -o Horde.vcf"

rule unify:
    input:
         rules.merge.output
    output:
          temp("ref_0.vcf.gz")

    shell:
         "bcftools +missing2ref {input} | bcftools +fill-tags | bgzip -c  > {output[0]} "

rule filter:
    input:
         rules.unify.output
    output:
          temp("filtered_minDP_10_minGQ_15.vcf")
    shell:
         "bcftools +setGT {input} -- -t q -i 'FORMAT/DP<4' -n . > {output}"

rule statistics:
    input:
         rules.filter.output
    output:
          "variant_statistics.tab.gz"
    shell:
         "bcftools query -f'%CHROM\t%POS\t%REF\t%ALT\t%AN\t%AC\t%AC_Hom\t%AC_Hemi\t%AC_Het\n' {input[0]} | sed 's/chr//g' | bgzip -c > {output} && tabix -p vcf {output}"
