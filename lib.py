

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
    zapusk = open('config.yaml')
    A = []

    for line in zapusk:
        a = 'grabix check' + line
        if subprocess.check_output(a, shell=True):
            a = 'bgzip ' + line + '; tabix ' + line + '.gz'
            subprocess.check_output(a, shell=True)
            gz_file_name = line + '.gz \n'
            A.append(gz_file_name)
        else:
            A.append(line)
    zapusk.close()
    file = open('config.yaml', 'a')
    file.write('zapusk:')
    for line in A:
        file.write('\n - ')
        file.write(line)
    return 0