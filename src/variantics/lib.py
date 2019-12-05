import os
import subprocess


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
            gzline = line.replace('.vcf', '.vcf.gz')
            a = 'tabix ' + gzline + '\n'
            subprocess.check_output(a, shell=True)
            gz_file_name = gzline + '\n'
            A.append(gz_file_name)
        else:
            A.append(line)
    zapusk.close()
    print(A)
    data_list_path = "data_list1"
    with open(data_list_path, 'w') as f:
        for line in A:
            f.writelines([os.path.abspath(line.replace("\n", "")) + "\n"])
    return 0


def prepare(args):
    a = "snakemake variant_statistics.tab.gz"
    subprocess.check_output(a, shell=True)


import pandas
import numpy as np
from cyvcf2 import VCF, Writer
import json
from sklearn.preprocessing import OrdinalEncoder
from variantics.constants import Bins, categorial_metadata, sample_name, TrueBins, imp_meta


def hist(vhod, meta, vihod):
    vcf_in = reading(vhod)
    vcf_out = Writer(vihod, vcf_in)
    result = prepare_meta(meta)
    for rec in vcf_in:
        DPM = prepare_DP(rec)
        A = makeHist(result, DPM)
        ANM = prepare_AN(rec)
        B = makeHist(result, ANM)
        ACM = prepare_AC(rec)
        C = makeHist(result, ACM)
        VARIANTICS_HIST = json.dumps(
            {
                'DP_HIST': {
                    'hist': A[0].tolist(),
                    'edges': inverse(A[1])
                },
                'AN_HIST': {
                    'hist': B[0].tolist(),
                    'edges': inverse(B[1])
                },
                'AC_HIST': {
                    'hist': C[0].tolist(),
                    'edges': inverse(C[1])
                }
            }
        )
        rec.INFO["VARIANTICS_HIST"] = VARIANTICS_HIST
        vcf_out.write_record(rec)
    vcf_in.close()
    vcf_out.close()
    return vihod


def reading(vhod):
    vcf_in = VCF(vhod)
    vcf_in.add_info_to_header(
        {
            'ID': 'VARIANTICS_HIST',
            'Description': 'Dict of histograms',
            'Type': 'String',
            'Number': 1
        }
    )
    return vcf_in


def prepare_meta(meta):
    csv = pandas.read_csv(meta, sep=',')
    enc = OrdinalEncoder()
    X = csv.loc[:, categorial_metadata]
    enc.fit(X)
    Y = pandas.DataFrame(enc.transform(X), columns=categorial_metadata)
    for feature in categorial_metadata:
        csv[feature] = Y[feature]
    csv.index = csv[sample_name]
    csv = csv[imp_meta]
    return csv


def prepare_DP(rec):
    return [
        max(rec[0], 0) for rec in rec.format('DP')
    ]


def prepare_AN(rec):
    return [
        2 if sample != 2 else 0 for sample in rec.gt_types
    ]


def prepare_AC(rec):
    # gt_types is array of 0,1,2,3==HOM_REF, HET, UNKNOWN, HOM_ALT
    gt2ac = {
        1: 1,
        3: 2,
        2: 0,
        0: 0
    }
    return [
        gt2ac[gt] for gt in rec.gt_types
    ]


def makeHist(result, weight):
    A = np.histogramdd(result.values, bins=Bins, weights=weight)
    for j in range(len(A[1])):
        A[1][j] = A[1][j].tolist()
    return A


def inverse(MasBin):
    NewMasBin = []
    for j in range(1, len(MasBin)):
        for i in range(len(MasBin[j]) - 1):
            MasBin[j][i] = TrueBins[j][i]
        MasBin[j].pop()
    NewMasBin.append(MasBin[0])
    NewMasBin.append(MasBin[1])
    NewMasBin.append(MasBin[2])
    return NewMasBin
