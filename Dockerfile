FROM continuumio/anaconda3

RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y gettext autoconf automake make gcc perl zlib1g-dev libbz2-dev \
     liblzma-dev libcurl4-gnutls-dev libssl-dev git libopenblas-dev r-base

RUN conda install -c bioconda -c conda-forge snakemake bcftools grabix tabix

WORKDIR /app
RUN Rscript -e 'if (!requireNamespace("BiocManager", quietly = TRUE))' -e '  install.packages("BiocManager")' -e 'BiocManager::install("SNPRelate")'
ADD . /app
RUN pip install -r requirements.txt
RUN python setup.py install
