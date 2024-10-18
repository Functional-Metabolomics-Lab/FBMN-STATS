#!/bin/bash

# Notify the user
echo "This script may ask for your password to install required software."

# Check if Homebrew is installed; if not, install it
if ! command -v brew &> /dev/null
then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Adding Homebrew to PATH
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "Homebrew is already installed."
fi

# Ensure Homebrew is in the PATH for the current session
eval "$(/opt/homebrew/bin/brew shellenv)"

# Install Python if not installed
if ! command -v python3 &> /dev/null
then
    echo "Installing Python via Homebrew..."
    brew install python
else
    echo "Python is already installed."
fi

# Install R if not already installed
if ! command -v R &> /dev/null
then
    echo "Installing R..."
    brew install r
else
    echo "R is already installed."
fi

# Set up a Python virtual environment
if [ ! -d "my_env" ]
then
    echo "Setting up Python virtual environment..."
    python3 -m venv my_env
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source my_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies (JupyterLab)
echo "Installing JupyterLab and required Python packages..."
pip install jupyterlab

# Install R kernel for Jupyter
echo "Installing R Kernel for Jupyter..."
R -e "install.packages('IRkernel', repos='https://cloud.r-project.org/'); IRkernel::installspec()"

# Install any additional R packages required by the user
R -e "install.packages(c('crayon', 'devtools', 'git2r', 'uuid', 'digest', 'pbdZMQ'), repos='https://cloud.r-project.org/')"

# Done message
echo "Setup complete! To start JupyterLab, run the following commands:"
echo "source my_env/bin/activate"
echo "jupyter lab"
