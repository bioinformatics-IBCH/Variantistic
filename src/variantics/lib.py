import os
import subprocess
from pysam import VariantFile
import pandas
import numpy as np
import matplotlib.pyplot as plt
import sys

def check_gz(args):

        zapusk = open(args.data)
        A = []
        for line in zapusk:
            a = 'grabix check ' + line
            print(line)
            if subprocess.check_output(a, shell=True) == b'no\n':
                a = 'bgzip ' + line
                print(a)
                subprocess.check_output(a, shell=True)
                gzline = line.replace('.vcf','.vcf.gz')
                a = 'tabix ' + gzline + '\n'
                subprocess.check_output(a, shell=True)
                gz_file_name = gzline  + '\n'
                A.append(gz_file_name)
            else:
                A.append(line)
        zapusk.close()
        print(A)
        data_list_path =  "data_list1"
        with open(data_list_path, 'w') as f:
            for line in A:
                f.writelines([os.path.abspath(line.replace("\n", "")) + "\n"])
        return 0



def prepare(args):
    a = "snakemake variant_statistics.tab.gz"
    subprocess.check_output(a, shell=True)


