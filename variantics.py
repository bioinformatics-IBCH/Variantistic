
import argparse
import os
import subprocess
from os.path import basename


parser = argparse.ArgumentParser()
parser.add_argument("--vcf", type=str, action="store", help="input vcf data")
parser.add_argument("--output", type=str, action="store", help="output directory")
parser.add_argument("--type", type=str, action="store", help="type")
args = parser.parse_args()

if args.type == 'WES':

	
	
	vcf = open(args.vcf)
	vcf1 = vcf.readline()
	vcf.close()
	if vcf1[0] == '#':
		name = args.output + '/' + 'zapusk.txt'
		file = open(name,'w')
		file.write(args.vcf)
		file.close()
	else:
		a = 'cp ' + args.vcf + ' ' + args.output + '/zapusk.txt'
		subprocess.check_output(a, shell=True)
	a = 'cp script1.py '+ args.output + '/script1.py;' + 'cp Snakefile ' + args.output + '/Snakefile; cd ' + args.output + '; snakemake --use-conda variant_statistics.tab.gz'
	subprocess.check_output(a, shell=True)

else:
	print('Unsupported data type.')
