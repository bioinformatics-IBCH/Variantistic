# variantics

[![Build status](https://travis-ci.com/bioinformatics-IBCH/variantics.svg?branch=master)](https://travis-ci.com/bioinformatics-IBCH/variantics)




#Usage
## Parametrs
--data location of input text file, where rows are paths to VCF files

--output location of output folder

--type type of input data
## Output files
variant_statistics.tab.gz - main final file with data
PCA.tsv - table with PCA data
PCA.png - image with PCA 
## For instance:
 `python variantics.py prepare --data 'list.txt' --output 'output_folder' --type WES`

