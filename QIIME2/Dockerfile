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
RUN /bin/bash -c ". activate qiime2 && pip install git+https://github.com/Wang-Bioinformatics-Lab/GNPSDataPackage.git@52d76594eeffee6fe3eba16c58e9f7800a6c9225"
RUN /bin/bash -c ". activate qiime2 && jupyter serverextension enable --py qiime2 --sys-prefix"

# Installing Specific Plugins for Metabolomics
RUN /bin/bash -c ". activate qiime2 && pip install git+https://github.com/Wang-Bioinformatics-Lab/qiime2_normalization_plugin.git@d695201694191eb168942124bea1faca80f7ffc2"
RUN /bin/bash -c ". activate qiime2 && pip install git+https://github.com/Wang-Bioinformatics-Lab/qiime2_imputation_plugin.git@edce69bce04cd653ec22b4ee0327af366a278106"
RUN /bin/bash -c ". activate qiime2 && pip install git+https://github.com/Wang-Bioinformatics-Lab/qiime2_blank_removal_plugin.git@d9b947497530702b6f396e8918c8ce27055650f7"

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

WORKDIR /home/${NB_USER}/