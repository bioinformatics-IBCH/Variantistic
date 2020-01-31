# -*- coding: utf-8 -*-

import sys
import argparse
import os
import json

from exitstatus import ExitStatus

from variantics.constants import VarianticsCommands
from variantics.lib import prepare, check_gz


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    pipeline_parser = subparsers.add_parser(
        VarianticsCommands.PREPARE.value, help='Prepares input genomic data for uploading to RE project',
    )
    pipeline_parser.add_argument('--data', type=str, action='store', help='input vcf data')
    pipeline_parser.add_argument('--output', type=str, action='store', help='output directory')
    pipeline_parser.add_argument('--type', choices=['WES'], default='WES', type=str, action='store', help='type')

    check_gz_parser = subparsers.add_parser(
        VarianticsCommands.CHECK_GZ.value,
        help='BGzip and index input vcf if needed',
    )
    check_gz_parser.add_argument('--data', type=str, action='store', help='input data list')

    create_histograms_parser = subparsers.add_parser(
        VarianticsCommands.CREATE_HISTOGRAMS.value,
        help='Create multidimensional histograms',
    )
    create_histograms_parser.add_argument("--data", type=str, action="store", help="input vcf data")
    create_histograms_parser.add_argument("--meta", type=str, action="store", help="metadataset")
    create_histograms_parser.add_argument("--output", type=str, action="store", help="output data with histogram lists")
    return parser.parse_args()


def ensure_folder_exists(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


def main() -> ExitStatus:
    args = parse_args()
    if args.command == 'prepare':
        ensure_folder_exists(args.output)
        data_list_path = os.path.join(args.output, 'data_list')
        config = {
            'var': 'variantics',
            'results_folder': args.output,
            'input_data': 'data_list',
            'upgrade_input_data': 'data_list1'
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

        prepare(args)
    else:
        eval(args.command)(args)

    return ExitStatus.success


if __name__ == '__main__':
    sys.exit(main())
