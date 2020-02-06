# variantics

[![Build status](https://travis-ci.com/bioinformatics-IBCH/variantics.svg?branch=master)](https://travis-ci.com/bioinformatics-IBCH/variantics)

## Prerequisite

Variantics is distributed through the docker container since it uses various libraries and tools in a unified environment,
so it is implied that a [docker engine](https://docs.docker.com/install/) is installed.

## Getting started

```bash
# pull latest version of container
docker pull dezzan/variantics:latest

# run application
docker run -v $(PWD)/input/:/input -v $(PWD)/results/:/results dezzan/variantics variantics prepare --data /input/multisample.vcf --output /results/output --metadata /input/metadata.csv
```

## Input data

Variantics can use two types of files as an input:
1. Multisample VCF file
2. Text file with list of absolute paths to the single/multisample VCFs, each on new line. This option could be used to feed any amount of data as an input.   

```text
/path/to/sample1.vcf
/path/to/sample2.vcf
...
```
## Meta data

Meta data input table consists of 4 obligatory columns and any number of additional columns. It is used only during the
processing steps and no personal data from this table is packed in the resulting archive. Typically, meta data could be 
presented in the following way:

 Sample name | Age | Phenotype | Sex | Diseased | Relativeness
 --- | --- | --- | --- | --- | ---
 Sample 1 | 12 | P1 | M | Healthy | 1
 Sample 2 | 25 | P2 | F | Diseased | 1
 Sample 3 | 39 | P2 | M | Diseased | 2 


Expected types and possible values of obligatory parameters are presented in the table below.

Parameter | Description | Type or possible values
--- | --- | ---
Sample name | the name of the sample as written in input VCF file | String 
Age | - |  Any number in range [-1000, 1000]
Phenotype | Any short description of sample phenotype | Any string
Sex | - | Male, Female, Unknown encoded as an element of set {M, F, U}
Diseased | - | {Diseased, Healthy, Unknown}
Relativeness | represents relativeness between samples in the dataset (same value = related samples) | Any string or number 


## Testing
To run the tests invoke ```tox``` command
