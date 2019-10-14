
import subprocess

zapusk = open(str(snakemake.input))
file = open('zapusk2.txt', 'w')		
for i in zapusk:
	a = 'grabix check' + i
	print(i,' ',subprocess.check_output(a, shell=True))
	if subprocess.check_output(a, shell=True):
		a = 'bgzip ' + i + '; tabix ' + i + '.gz'
		subprocess.check_output(a, shell=True)
		b = i + '.gz \n'
		file.write(b)
	else:
		file.write(i)
file.close()