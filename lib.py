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

    x = args.meta
    metadata = pandas.read_csv(x, sep=',')  # начало сортировки
    a = ("Sample name", "Age")
    B = metadata.loc[:, a]

    for rec in vcf.fetch():
        DPM = []
        A = rec.samples.keys()
        try:
            for i in A:
                DPM.append(rec.samples[i]["DP"])
            A, B = np.histogram(DPM, bins=[i for i in range(1, 200, 10)])   # создание и запись гистограмм
            #plt.bar(B[:-1], A, width=1)
            #plt.xlim(min(B), max(B))                                       # нарисование гистограмм
            #plt.show()
        except:
            print('Не работает!')
