FROM continuumio/anaconda3

RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y gettext autoconf automake make gcc perl zlib1g-dev libbz2-dev liblzma-dev libcurl4-gnutls-dev libssl-dev git libopenblas-dev

RUN conda install -c bioconda -c conda-forge snakemake bcftools grabix tabix

WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app
RUN python setup.py install
