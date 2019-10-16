
from exitstatus import ExitStatus
import sys
import argparse
import os
import subprocess
from os.path import basename

def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser()
	parser.add_argument("--vcf", type=str, action="store", help="input vcf data")
	parser.add_argument("--output", type=str, action="store", help="output directory")
	parser.add_argument("--type", type=str, action="store", help="type")
	args = parser.parse_args()
	return parser.parse_args()



def main() -> ExitStatus:

	args = parse_args()
	if args.type == 'WES':

		vcf = open(args.vcf)
		vcf_first_line = vcf.readline()
		vcf.close()
		if vcf_first_line[0] == '#':
			name_output = args.output + '/' + 'zapusk.txt'
			file = open(name_output,'w')
			file.write(args.vcf)
			file.close()
		else:
			a = 'cp ' + args.vcf + ' ' + args.output + '/zapusk.txt'
			subprocess.check_output(a, shell=True)

		a = 'cp WriteListVcf.py '+ args.output + '/WriteListVcf.py;' + 'cp Snakefile ' + args.output + '/Snakefile; cd ' + args.output + '; snakemake --use-conda variant_statistics.tab.gz'
		subprocess.check_output(a, shell=True)

	else:
		print('Unsupported data type.')

	return ExitStatus.success


if __name__ == '__main__':
    sys.exit(main())