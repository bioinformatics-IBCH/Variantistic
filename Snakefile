configfile: "config.json"
workdir: config["results_folder"]

rule check_files_are_gzipped:
    input:
         config["input_data"],
    output:
          config["processed_vcf_list"]
    shell:
         "variantics check_gz --data {input} --output {output}"

rule merge:
    input:
         rules.check_files_are_gzipped.output
    output:
          temp("merged.vcf")
    shell:
         "bcftools merge -m all -i AC:sum,AN:sum --force-samples -l {input} -o {output}"

rule unify:
    input:
         rules.merge.output
    output:
          temp("filled_tags.vcf.gz")

    shell:
         "bcftools +missing2ref {input} | bcftools +fill-tags | bgzip -c  > {output} "

rule filter:
    input:
         rules.unify.output
    output:
          temp("filtered.vcf")
    shell:
         "bcftools +setGT {input} -- -t q -i 'FORMAT/DP<4' -n . > {output}"

rule create_histograms:
    input:
        data=rules.filter.output, metadata=config["metadata"]
    output:
        temp("histograms.vcf")
    shell:
        "variantics create_histograms --data {input.data} --metadata {input.metadata} --output {output}"

rule plot_pca:
    input:
        rules.filter.output
    output:
        "PCA.png"
    shell:
        "Rscript /app/src/variantics/pca.R {input} PCA"

rule statistics:
    input:
         rules.create_histograms.output
    output:
          "variant_statistics.tab.gz"
    shell:
         "bcftools query -f'%CHROM\t%POS\t%REF\t%ALT\t%AN\t%AC\t%AC_Hom\t%AC_Hemi\t%AC_Het\t%VARIANTICS_HIST\n' {input} | sed 's/chr//g' | bgzip -c > {output} && tabix -p vcf {output}"
