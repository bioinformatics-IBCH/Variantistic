import os
import json
import subprocess

from cyvcf2 import VCF, Writer
import numpy as np
import pandas
from sklearn.preprocessing import OrdinalEncoder

from variantics.constants import (
    CATEGORICAL_METADATA,
    SAMPLE_NAME_COLUMN,
    METADATA_VALID_VALUES,
    CATEGORY_BINS,
    BINS
)


def check_gz(args):
    zapusk = open(args.data)
    gzipped_data_list = []
    for line in zapusk:
        a = 'grabix check ' + line
        if subprocess.check_output(a, shell=True) == b'no\n':
            a = 'bgzip ' + line
            subprocess.check_output(a, shell=True)
            gzline = line.replace('.vcf', '.vcf.gz')
            a = 'tabix ' + gzline + '\n'
            subprocess.check_output(a, shell=True)
            gz_file_name = gzline + '\n'
            gzipped_data_list.append(gz_file_name)
        else:
            gzipped_data_list.append(line)
    zapusk.close()
    data_list_path = 'data_list1'
    with open(data_list_path, 'w') as f:
        for line in gzipped_data_list:
            f.writelines([os.path.abspath(line.replace('\n', '')) + '\n'])
    return 0


def prepare(args):
    cmd = 'snakemake variant_statistics.tab.gz'
    subprocess.check_output(cmd, shell=True)


def hist(vhod, meta, vihod):
    vcf_in = reading(vhod)
    vcf_out = Writer(vihod, vcf_in)
    result = prepare_meta(meta)
    for rec in vcf_in:
        dpm = prepare_dp(rec)
        dpm_hist = make_hist(result, dpm)
        anm = prepare_an(rec)
        anm_hist = make_hist(result, anm)
        acm = prepare_ac(rec)
        acm_hist = make_hist(result, acm)
        variantics_hist = json.dumps(
            {
                'DP_HIST': {
                    'hist': dpm_hist[0].tolist(),
                    'edges': inverse(dpm_hist[1])
                },
                'AN_HIST': {
                    'hist': anm_hist[0].tolist(),
                    'edges': inverse(anm_hist[1])
                },
                'AC_HIST': {
                    'hist': acm_hist[0].tolist(),
                    'edges': inverse(acm_hist[1])
                }
            }
        )
        rec.INFO['VARIANTICS_HIST'] = variantics_hist
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
    categ_meta = csv.loc[:, CATEGORICAL_METADATA]
    enc.fit(categ_meta)
    transformed_meta = pandas.DataFrame(enc.transform(categ_meta), columns=CATEGORICAL_METADATA)
    for feature in CATEGORICAL_METADATA:
        csv[feature] = transformed_meta[feature]
    csv.index = csv[SAMPLE_NAME_COLUMN]
    csv = csv[METADATA_VALID_VALUES.keys()]
    return csv


def prepare_dp(rec):
    return [
        max(rec[0], 0) for rec in rec.format('DP')
    ]


def prepare_an(rec):
    return [
        2 if sample != 2 else 0 for sample in rec.gt_types
    ]


def prepare_ac(rec):
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


def make_hist(result, weight):
    histogram = np.histogramdd(result.values, bins=BINS, weights=weight)
    for j in range(len(histogram[1])):
        histogram[1][j] = histogram[1][j].tolist()
    return histogram


def inverse(mas_bin):
    new_mas_bin = []
    for j in range(1, len(mas_bin)):
        for i in range(len(mas_bin[j]) - 1):
            mas_bin[j][i] = CATEGORY_BINS[j][i]
        mas_bin[j].pop()
    new_mas_bin.append(mas_bin[0])
    new_mas_bin.append(mas_bin[1])
    new_mas_bin.append(mas_bin[2])
    return new_mas_bin
