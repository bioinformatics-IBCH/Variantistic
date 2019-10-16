
import subprocess

zapusk = open(str(snakemake.input))
file = open('zapusk2.txt', 'w')		
for line in zapusk:
	a = 'grabix check' + line
	if subprocess.check_output(a, shell=True):
		a = 'bgzip ' + line + '; tabix ' + i + '.gz'
		subprocess.check_output(a, shell=True)
		gz_file_name = line + '.gz \n'
		file.write(gz_file_name)
	else:
		file.write(line)
file.close()