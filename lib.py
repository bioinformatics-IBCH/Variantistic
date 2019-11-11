import os
import subprocess
from pysam import VariantFile
import pandas
import numpy as np
import matplotlib.pyplot as plt


def check_gz(args):
    zapusk = open(args.data)
    A = []
    for line in zapusk:
        a = 'grabix check' + line
        if subprocess.check_output(a, shell=True):
            a = 'bgzip ' + line + '; tabix ' + line + '.gz'
            subprocess.check_output(a, shell=True)
            gz_file_name = line + '.gz \n'
            A.append(gz_file_name)
        else:
            A.append(line)
    zapusk.close()
    data_list_path = "data_list"
    with open(data_list_path, 'w') as f:
        for line in A:
            f.writelines([os.path.abspath(line.replace("\n", "")) + "\n"])
    return 0


def prepare(args):
    a = 'snakemake variant_statistics.tab.gz'
    subprocess.check_output(a, shell=True)


def hist(args):

    vcf = VariantFile(args.data)
    csv = pandas.read_csv(args.meta, sep=',')
    output_vcf = open(args.output + '/MergeWithHist.vcf', 'w')
    for rec in vcf.fetch():
        DPM = []
        ACM = []
        ANM = []
        A = rec.samples.keys()

        for i in A:
            AC = 0
            AN = 0
            if rec.samples[i]["DP"] is not None:
                DPM.append(rec.samples[i]["DP"])
            else:
                DPM.append(0)
            GT = rec.samples[i]["GT"]

            for j in GT:

                if j == 1:
                    AC += 1
                    AN += 1
                elif j == 0:
                    AN += 1
            ACM.append(AC)
            ANM.append(AN)
        result = pandas.DataFrame({
            "Age": csv.Age.tolist(),
            "DiseaseId": csv.DiseaseId.tolist(),
            # "Relativeness": csv.Relativeness,
            # "DP": DPM,
            # "AN": ANM,
            #         "AC": ACM
        }, index=csv["Sample name"])
        result = np.array(result)

        bins = np.asarray([4, 4])                     # бины надо построить
        A = np.histogramdd(result, bins=bins, weights=DPM)
        B = np.histogramdd(result, bins=bins, weights=ANM)
        C = np.histogramdd(result, bins=bins, weights=ACM)
        a = (str(rec) + ';' + str(A) + ';' + str(B) + ';' + str(C)).replace('\n', '\t')    # здесь строится строка для записи, напиши, если она должна строиться по-другому
        output_vcf.write(a)
    output_vcf.close()