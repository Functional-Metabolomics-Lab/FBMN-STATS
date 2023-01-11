# Statistical-analysis-of-non-targeted-LC-MS-MS-data:
This repository contains the test data and the notebooks for the paper 'A hitchhiker's guide to statistical analysis of non-targeted LC-MS/MS data'

The result files of the notebook can be found in the Google Drive:
[Google Drive Link for the files](https://drive.google.com/drive/folders/1qHAdvDGr9Kre0SK3AMc1Dzfu6XeFE48A?usp=sharing) <br>
[Link for Feature-Based Molecular Network](https://gnps.ucsd.edu/ProteoSAFe/status.jsp?task=cf6e14abf5604f47b28b467a513d3532) <br>

<b>MASSIVE Datasets from which all the files were selected for MZmine3 </b>: 
[MSV000082312](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=8a81) and [MSV000085786](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=c8411b76f30a4f4ca5d3e42ec13998dc) <br>


## Google Colab:
This Notebook can be also executed using Google Colab, a cloud environment for running Jupyter Notebooks and scripts. It is commonly used with Python and comes pre-installed with all essential Python packages. However, we can also run Colab with R. Basic requirement for using Colab is to have a google account. No extra installation in your computer is needed as such for Jupyter Notebook. To execute our notebook in Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Functional-Metabolomics-Lab/Statistical-analysis-of-non-targeted-LC-MSMS-data/blob/main) <br>

In Colab, before starting to run this notebook with your own data, save a copy of this notebook in your own Google Drive by clicking on <b> File &rarr; Save a copy in Drive. </b> You can give whatever meaningful name to your notebook. You can find this newly created file under the folder  <b> 'Colab Notebooks'</b> in your Drive. 

## For first time Colab users, some useful information to note:

### 1. Package Installation:
Since Colab does not come pre-installed with R packages (or libraries), when running our R Notebook in Colab, we need to install the packages every time we run the notebook and the installation might take some time. However, direct Jupyter Notebook users need to install it only once as it is installed locally.

### 2. Setting a working directory:
![Google-Colab Files Upload](https://github.com/abzer005/Images-for-Jupyter-Notebooks/blob/main/StepsAll.png?raw=true)
- As Colab is cloud-based, it is not possible to access the files from your local computer like in Jupyter Notebook. So we can directly upload the necessary files into the Colab using the <b>'Files icon'</b> on the left corner of your Colab space as shown in the image. 
- Then we can create a new folder called 'My_TestData' in the Colab space and set it as working directory. 
```
dir.create("/content/My_TestData", showWarnings = TRUE, recursive = FALSE, mode = "0777") #creating a folder
setwd("/content/My_TestData") 
```
Following the steps in the image, you can check in your Colab to see if the folder has been created. Once you see it, simply upload the files from your local PC to the folder 'My_TestData' and then continue running the rest of the script.
<b>All the files uploaded to Google Colab would generally disappear after 12 hours. Similarly, all the outputs would be saved only in the Colab, so we need to download them into our local system at the end of our session.</b>
