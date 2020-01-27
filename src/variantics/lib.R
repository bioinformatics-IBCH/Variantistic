#!/usr/bin/env Rscript


library(gdsfmt)
library(SNPRelate)

PCA = function(vcf = NA,
               out = NA) 
{
    print(vcf)
    print(out)
    vcf.fn <- vcf
    tail <- ".gds"
    tail1 <- ".tsv"
    tail2 <- ".png"
    snpgdsVCF2GDS(vcf.fn, paste(vcf,tail, sep = ""), method="biallelic.only")
    snpgdsSummary(paste(vcf.fn,tail, sep = ""))
    genofile <- snpgdsOpen(paste(vcf.fn,tail, sep = ""))
    snpset <- snpgdsLDpruning(genofile, ld.threshold=0.2)
    snpset.id <- unlist(snpset)
    pca <- snpgdsPCA(genofile, snp.id=snpset.id, num.thread=2)
    pc.percent <- pca$varprop*100
    tab <- data.frame(sample.id = pca$sample.id,
                     EV1 = pca$eigenvect[,1],    # the first eigenvector
                     EV2 = pca$eigenvect[,2],    # the second eigenvector
                     stringsAsFactors = FALSE)
    write(paste(tab$EV1,tab$EV2), file = paste(out,tail1, sep = ""), sep = "\t")
    png(filename=paste(out,tail2, sep = ""))
    plot(tab$EV2, tab$EV1, xlab="eigenvector 2", ylab="eigenvector 1")
    dev.off()
    return(paste(out,tail1, sep = ""))
}
args = commandArgs(trailingOnly=TRUE)

PCA(args[1],args[2])