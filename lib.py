import os
import subprocess
from pysam import VariantFile
import pandas
import numpy as np
import matplotlib.pyplot as plt




def check_gz(args):
    zapusk = open('config.json')
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
    file = open('config.yaml', 'a')
    file.write('zapusk:')
    for line in A:
        file.write('\n - ')
        file.write(line)
    return 0


def prepare(args):
    a = 'snakemake variant_statistics.tab.gz'
    subprocess.check_output(a, shell=True)

def hist(args):

    vcf = VariantFile(args.data)
    csv = pandas.read_csv(args.meta, sep=',')
    for rec in vcf.fetch():
        DPM = []
        ACM = []
        ANM = []
        A = rec.samples.keys()

        for i in A:
            AC = 0
            AN = 0
            DPM.append(rec.samples[i]["DP"])
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
            "Age": csv.Age,
            "Phenotype": csv.Phenotype,
            "Sex": csv.Sex,
            "DiseaseId": csv.DiseaseId,
            "Relativeness": csv.Relativeness,
            "DP": DPM,
            "AN": ANM,
            "AC": ACM
        }, index=csv["Sample name"])



        result = np.array(result)

        bins = np.asarray([10, 2, 2, 30, 40, 40, 50, 50])              # корзины надо честно прописать

        B = np.histogramdd(result, bins=bins, range=([1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2]))   # range нужно наверное, тоже нормально прописать
