## Running Locally without Docker

### Download the repository 
git clone https://github.com/Functional-Metabolomics-Lab/FBMN-STATS.git

### Navigate to the repository folder
cd FBMN-STATS/QIIME2/

### Installing Mamba
conda install -c conda-forge mamba

wget https://data.qiime2.org/distro/core/qiime2-2023.2-py38-linux-conda.yml
mamba env create -n qiime2 --file qiime2-2023.2-py38-linux-conda.yml

conda activate qiime2
pip install -r requirements.txt

### Installing GNPS Data Package
pip install git+https://github.com/Wang-Bioinformatics-Lab/GNPSDataPackage.git@2035cd2aa27dd29e311c7a9e171abf7f2207789a

### Prepping the notebooks
jupyter serverextension enable --py qiime2 --sys-prefix

jupyter lab


## Running with Docker

Download [Docker](https://www.docker.com/), docker-compose, and git, then follow the steps below.

1. Clone the repository - run "git clone https://github.com/Functional-Metabolomics-Lab/FBMN-STATS.git"
1. Go to Qiime directory - cd QIIME2
1. Bring up Docker - ```make jupyter-compose```
1. Connect to the Jupyter Notebook at http://localhost:9574/, the default token is "PASSWORD"

