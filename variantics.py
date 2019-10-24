# -*- coding: utf-8 -*-

from lib import check_gz, propusk
from exitstatus import ExitStatus
import sys
import argparse
import os
import subprocess

FUNCTION_MAP = { 'check_gz': check_gz,
			'start': propusk}


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser()
	parser.add_argument('command', choices=FUNCTION_MAP.keys())
	parser.add_argument("--vcf", type=str, action="store", help="input vcf data")
	parser.add_argument("--output", type=str, action="store", help="output directory")
	parser.add_argument("--type",choices=['WES'], type=str, action="store", help="type")
	return parser.parse_args()


def main() -> ExitStatus:
	args = parse_args()
	output = open('config.yaml', 'w')
	if args.output is not None:
		output.write('vivod:\n - ')
		output.write(args.output)
		output.write('\n')
	func = FUNCTION_MAP[args.command]
	func(args)
	if args.type is not None:
		vcf = open(args.vcf)
		vcf_first_line = vcf.readline()
		output.write('no_check:')
		if vcf_first_line[0] == '#':
			output.write('\n - ')
			output.write(args.vcf)
		else:
			output.write('\n - ')
			output.write(vcf_first_line)
			for line in vcf:
				output.write(' - ')
				output.write(line)
		vcf.close()
		a = 'snakemake --use-conda variant_statistics.tab.gz'
		subprocess.check_output(a, shell=True)
	output.close()
	return ExitStatus.success


if __name__ == '__main__':
	sys.exit(main())