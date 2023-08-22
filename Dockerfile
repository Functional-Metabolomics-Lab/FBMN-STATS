# Use the base Miniconda image
FROM continuumio/miniconda3

# Set working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY /QIIME2/requirements.txt /app/requirements.txt

COPY /QIIME2/QIIME2

# Download the Qiime2 environment YAML file
RUN wget https://data.qiime2.org/distro/core/qiime2-2023.2-py38-linux-conda.yml -O qiime2_env.yml

# Update Conda
RUN conda update -n base -c defaults conda

# Install required packages via conda from the Qiime2 environment YAML file
RUN conda env create -n qiime2 --file qiime2_env.yml

# Activate the qiime2 environment and install pip requirements
SHELL ["conda", "run", "-n", "qiime2", "/bin/bash", "-c", "pip install -r /app/requirements.txt && pip install git+https://github.com/Wang-Bioinformatics-Lab/GNPSDataPackage.git@2035cd2aa27dd29e311c7a9e171abf7f2207789a"]

# Enable the Qiime2 Jupyter Notebook serverextension
RUN conda run -n qiime2 jupyter serverextension enable --py qiime2 --sys-prefix

# Install Jupyter Notebook and ipykernel in the qiime2 environment
RUN conda install -n qiime2 jupyter ipykernel
# Download the Qiime2 environment YAML file
RUN wget https://data.qiime2.org/distro/core/qiime2-2023.2-py38-linux-conda.yml -O qiime2_env.yml

# Update Conda
RUN conda update -n base -c defaults conda

# Install required packages via conda from the Qiime2 environment YAML file
RUN conda env create -n qiime2 --file qiime2_env.yml

# Activate the qiime2 environment and install pip requirements
SHELL ["conda", "run", "-n", "qiime2", "/bin/bash", "-c", "pip install -r /app/requirements.txt && pip install git+https://github.com/Wang-Bioinformatics-Lab/GNPSDataPackage.git@2035cd2aa27dd29e311c7a9e171abf7f2207789a"]

# Enable the Qiime2 Jupyter Notebook extension
SHELL ["conda", "run", "-n", "qiime2", "/bin/bash", "-c", "jupyter serverextension enable --py qiime2 --sys-prefix"]

# Install Jupyter Notebook and ipykernel in the qiime2 environment
RUN conda install -n qiime2 jupyter ipykernel

# Set up a password (optional)
ARG JUPYTER_PASSWORD="qiime2"
RUN echo "c.NotebookApp.password = '$JUPYTER_PASSWORD'" >> ~/.jupyter/jupyter_notebook_config.py

# Expose the Jupyter port
EXPOSE 8888

# Start Jupyter Notebook when the container starts
CMD ["conda", "run", "-n", "qiime2", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=password"]
