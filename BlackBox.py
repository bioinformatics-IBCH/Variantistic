

import os
import subprocess
from os.path import basename


print('Введите директорию vcf:')
#x = str(input())
x = '/home/Welekie/Cursed'

Papka = os.listdir(x)

print('Введите директорию для вывода:')
#y = str(input())
y = '/home/Welekie/newworkspace/variantics/vivod'


name = y + '/' + 'zapusk.txt'
file = open(name,'w')

for i in Papka:
	p = i.split('.')
	t = p[-1]
	if t == 'gz':
		b = x + '/' + basename(i) + '\n'
		file.write(b)
	elif t != 'tbi':
		a = 'bgzip ' + x + '/' + basename(i) + '; tabix ' + x + '/' + basename(i) + '.gz'
		subprocess.check_output(a, shell=True)
file.close()



a = 'cp Snakefile ' + y + '/Snakefile; cd ' + y + '; snakemake --use-conda Vivod.tab.gz'
subprocess.check_output(a, shell=True)


