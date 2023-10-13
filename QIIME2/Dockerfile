FROM ubuntu:22.04

# Making sure we have libarchive
RUN apt-get update && apt-get install -y build-essential libarchive-dev wget vim git

# Install Mamba
ENV CONDA_DIR /opt/conda
RUN wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O ~/miniforge.sh && /bin/bash ~/miniforge.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

# Adding to bashrc
RUN echo "export PATH=$CONDA_DIR:$PATH" >> ~/.bashrc

# Installing Qiime2
RUN wget https://data.qiime2.org/distro/core/qiime2-2023.2-py38-linux-conda.yml
RUN mamba env create -n qiime2 --file qiime2-2023.2-py38-linux-conda.yml

COPY requirements.txt /
RUN /bin/bash -c ". activate qiime2 && pip install -r /requirements.txt"

# Installing GNPS Data Package
RUN /bin/bash -c ". activate qiime2 && pip install git+https://github.com/Wang-Bioinformatics-Lab/GNPSDataPackage.git@2035cd2aa27dd29e311c7a9e171abf7f2207789a"

RUN /bin/bash -c ". activate qiime2 && jupyter serverextension enable --py qiime2 --sys-prefix"

# Installing Specific Plugins for Metabolomics
#RUN /bin/bash -c ". activate qiime2 && pip install git+https://github.com/pluckySquid/qiime2_normalization_plugin.git@d695201694191eb168942124bea1faca80f7ffc2"
#RUN /bin/bash -c ". activate qiime2 && pip install git+https://github.com/pluckySquid/qiime2_imputation_plugin.git@edce69bce04cd653ec22b4ee0327af366a278106"
#RUN /bin/bash -c ". activate qiime2 && pip install git+https://github.com/pluckySquid/qiime2_blank_removal_plugin.git@384c58f4a1a2b65308bbd494b52d7cbe54fdb889"

## Setting up the proper permissions
ARG NB_USER=jovyan
ARG NB_UID=1000
RUN useradd -u ${NB_UID} -s /bin/bash -m ${NB_USER}

ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

# # Make sure the contents of our repo are in ${HOME}
COPY . /home/${NB_USER}/
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}