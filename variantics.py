# -*- coding: utf-8 -*-


from exitstatus import ExitStatus
import sys
import argparse
import os
import subprocess

def remove(args):
	output = open('Const.txt')
	output_first_line = output.readline()
	output.close()
	a = ' cp ' + args.vcf + ' ' + os.path.join(output_first_line, 'variant_statistics.tab.gz')
	subprocess.check_output(a, shell=True)
	w = open('variant_statistics.tab.gz','w')
	w.close()
	a = ' cp ' + args.vcf +'.tbi ' + os.path.join(output_first_line, 'variant_statistics.tab.gz.tbi')
	subprocess.check_output(a, shell=True)

def propusk(args):
	return 0


def check_gz(args):
	zapusk = open(str(args.vcf))
	file = open('zapusk2.txt', 'w')
	for line in zapusk:
		a = 'grabix check' + line
		if subprocess.check_output(a, shell=True):
			a = 'bgzip ' + line + '; tabix ' + line + '.gz'
			subprocess.check_output(a, shell=True)
			gz_file_name = line + '.gz \n'
			file.write(gz_file_name)
		else:
			file.write(line)
	file.close()
	return 0

FUNCTION_MAP = {'remove': remove,
				'check_gz': check_gz,
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
	if args.output is not None:
		output = open('Const.txt','w')
		output.write(args.output)
		output.close()
	func = FUNCTION_MAP[args.command]
	func(args)
	if args.type is not None:
		vcf = open(args.vcf)
		vcf_first_line = vcf.readline()
		vcf.close()
		if vcf_first_line[0] == '#':
			file = open('zapusk.txt','w')
			file.write(args.vcf)
			file.close()
		else:
			a = 'cp ' + args.vcf + ' ' + 'zapusk.txt'
			subprocess.check_output(a, shell=True)
		a = 'snakemake --use-conda variant_statistics.tab.gz'
		subprocess.check_output(a, shell=True)
	return ExitStatus.success


if __name__ == '__main__':
	sys.exit(main())