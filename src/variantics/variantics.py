# -*- coding: utf-8 -*-

from lib import check_gz, prepare
from exitstatus import ExitStatus
import sys
import argparse
import os
import subprocess
import json



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    pipeline_parser = subparsers.add_parser(
        'prepare', help='Prepares input genomic data for uploading to RE project',
    )
    pipeline_parser.add_argument("--data", type=str, action="store", help="input vcf data")
    pipeline_parser.add_argument("--output", type=str, action="store", help="output directory")
    pipeline_parser.add_argument("--type", choices=['WES'], type=str, action="store", help="type")

    check_gz_parser = subparsers.add_parser(
        'check_gz', help='Check vcfs',
    )
    check_gz_parser.add_argument("--data", type=str, action="store", help="input data list")
    # check_gz_parser.add_argument("--output", type=str, action="store", help="output directory")
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
        data_list_path = os.path.join(args.output, "data_list")
        config = {
            "var":  str(os.path.dirname(os.path.realpath(sys.argv[0]))) + '/variantics.py' ,
            "results_folder": args.output,
            "input_data": "data_list",
            "upgrade_input_data": "data_list1"
        }

        with open(data_list_path, 'w') as f:
            f.writelines([
                os.path.abspath(line.replace("\n", "")) + "\n" for line in open(args.data, 'r').readlines()
            ])

        with open('config.json', 'w') as f:
            json.dump(config, f)

    eval(args.command)(args)

    return ExitStatus.success


if __name__ == '__main__':
    sys.exit(main())
