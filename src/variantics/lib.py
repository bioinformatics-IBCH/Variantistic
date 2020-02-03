import copy
import os
import json
import subprocess

from cyvcf2 import VCF, Writer
import numpy as np
import pandas

from variantics.constants import (
    SAMPLE_NAME_COLUMN,
    VARIANTICS_HIST_VCF_HEADER
)
from variantics.categories import CATEGORIES, BINS


def prepare(args):
    data_list_path = os.path.join(args.output, 'data_list')
    config = {
        'results_folder': args.output,
        'input_data': data_list_path,
        'processed_vcf_list': 'processed_vcf_list',
        'metadata': args.metadata
    }

    with open(data_list_path, 'w') as f:
        if not args.data.endswith('.vcf') and not args.data.endswith('.vcf.gz'):
            f.writelines([
                os.path.abspath(line.replace('\n', '')) + '\n' for line in open(args.data, 'r').readlines()
            ])
        else:
            f.write(os.path.abspath(args.data))

    with open('config.json', 'w') as f:
        json.dump(config, f)

    cmd = 'snakemake --verbose variant_statistics.tab.gz PCA.png'
    subprocess.check_output(cmd, shell=True)


def check_gz(args):
    with open(args.data, 'r') as input_data:
        gzipped_data_list = []
        for line in input_data:
            a = 'grabix check ' + line
            if subprocess.check_output(a, shell=True) == b'no\n':
                new_path = os.path.join(
                    os.path.dirname(os.path.abspath(args.data)),
                    os.path.basename(line) + '.gz'
                )
                subprocess.check_output(f'bgzip {line} -c > {new_path}', shell=True)
                subprocess.check_output(f'tabix {new_path}', shell=True)
                gzipped_data_list.append(new_path)
            else:
                gzipped_data_list.append(line)

    with open(args.output, 'w') as f:
        for line in gzipped_data_list:
            f.writelines([os.path.abspath(line.replace('\n', '')) + '\n'])

    return args.output


def read_vcf(vcf):
    vcf_obj = VCF(vcf)
    vcf_obj.add_info_to_header(VARIANTICS_HIST_VCF_HEADER)
    return vcf_obj


def read_metadata(metadata):
    if isinstance(metadata, pandas.DataFrame):
        return metadata
    elif metadata.endswith('.csv'):
        return pandas.read_csv(metadata)
    elif metadata.endswith('.xslx'):
        return pandas.read_excel(metadata)
    raise


class MetadataProcessor:
    """
    Encodes/decodes metadata categories to fit limitations of numpy.histogramdd
    """

    def __init__(self, csv):
        self.categories = copy.deepcopy(CATEGORIES)
        self.encoded_csv = self._encode(csv)

    def _encode(self, csv):
        """
        Encodes values for columns marked as categorical
        Args:
            csv: pandas.DataFrame with metadata
        Returns:
        """
        encoded_metadata = csv.loc[:, [SAMPLE_NAME_COLUMN] + [category.name for category in self.categories]]
        for category in self.categories:
            if category.categorical:
                encoded_metadata[category.name] = category.encoder.transform(csv[category.name])
        return encoded_metadata.set_index(SAMPLE_NAME_COLUMN)

    @staticmethod
    def decode(category, values):
        if category.encoder:
            nvalues = values
            if category.categorical:
                # the last value from the `values` is dropped since for categorical slices
                # a left most bin edge was added explicitly (check comment in the `Category` class)
                nvalues = values[:-1]
            return category.encoder.inverse_transform(nvalues).tolist()
        return values

    def _get_category_by_name(self, name):
        for category in self.categories:
            if category.name == name:
                return category

    def decode_by_name(self, name, values):
        category = self._get_category_by_name(name)
        if category:
            return self.decode(category, values)
        return values


def encode_metadata(metadata):
    csv = read_metadata(metadata)
    return MetadataProcessor(csv)


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


def make_hist(values, weights, bins=BINS):
    """
    Creates multidimensional histogram
    Args:
        bins:
        values:
        weights:
    Returns: bins, edges
    """
    bns, edges = np.histogramdd(values.values, bins=bins, weights=weights)
    return bns.tolist(), [array.tolist() for array in edges]


class HistogramCreator:
    PARAMETER_CONFIG = {
        'DP': {
            'callable': prepare_dp
        },
        'AN': {
            'callable': prepare_an
        },
        'AC': {
            'callable': prepare_ac
        },
    }

    def __init__(self, multisample_vcf, metadata, output_path):
        self.multisample_vcf = multisample_vcf
        self.metadata = metadata
        self.output_path = output_path
        self.processor = encode_metadata(metadata)

    def process_record(self, record, configuration):
        """
        Makes multidimensional histogram for input record according to parameter configuration
        Args:
            record:
            configuration:

        Returns:

        """
        prepared_data = configuration['callable'](record)
        bins, edges = make_hist(self.processor.encoded_csv, prepared_data)
        decoded_edges = [
            self.processor.decode_by_name(column, edge)
            for column, edge in zip(self.processor.encoded_csv.columns, edges)
        ]
        return bins, decoded_edges

    def __call__(self):
        vcf_in = read_vcf(self.multisample_vcf)
        vcf_out = Writer(self.output_path, vcf_in)
        variantics_hist = {}
        for rec in vcf_in:
            for parameter, configuration in self.PARAMETER_CONFIG.items():
                bins, edges = self.process_record(rec, configuration)
                variantics_hist[f'{parameter}_HIST'] = {
                    'bins': bins,
                    'edges': edges
                }
            rec.INFO['VARIANTICS_HIST'] = json.dumps(variantics_hist)
            vcf_out.write_record(rec)
        vcf_in.close()
        vcf_out.close()
        return self.output_path
