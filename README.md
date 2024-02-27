![Google-Colab Files Upload](https://github.com/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/logo/FBMN-STATS_logo2.png)

This repository contains the test data and the Jupyter notebooks for the paper [The Hitchhiker’s Guide to Statistical Analysis of Feature-based Molecular Networks from Non-Targeted Metabolomics Data](https://chemrxiv.org/engage/chemrxiv/article-details/6540eb2548dad23120c52242). <br> Using the notebooks provided here, one can perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks.

The result files of the notebook can be found in the Google Drive:
- [Google Drive Link for the files](https://drive.google.com/drive/folders/1qHAdvDGr9Kre0SK3AMc1Dzfu6XeFE48A?usp=sharing) <br>
- [Link for Feature-Based Molecular Network](https://gnps.ucsd.edu/ProteoSAFe/status.jsp?task=b661d12ba88745639664988329c1363e) <br>

<b>MASSIVE Datasets from which all the files were selected for MZmine3 </b>: 
[MSV000082312](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=8a8139d9248b43e0b0fda17495387756) and [MSV000085786](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=c8411b76f30a4f4ca5d3e42ec13998dc) <br>

To easily install and run Jupyter Notebook in R, [follow the steps in the document according to your preferred OS](https://github.com/Functional-Metabolomics-Lab/FBMN-STATS/tree/main/Jupyter-Notebook-Installation-Guides) <br>

## Running the Notebooks (R, Python) on the cloud using Google Colab:
This Notebook can be also executed using Google Colab, a cloud environment for running Jupyter Notebooks. It is commonly used with Python and comes pre-installed with all essential Python packages. However, we can also run Colab with R Notebooks. Basic requirement for using Colab is to have a google account. No extra installation in your computer is needed as such for Jupyter Notebook. 
- To execute our R notebook in Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/R/Stats_Untargeted_Metabolomics.ipynb) <br> 
- To execute our Python notebook in Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/Python/Stats_Untargeted_Metabolomics_python.ipynb) <br>
- To run the web app implementation of the notebooks, follow the links of the app hosted by different servers: [GNPS2](https://fbmn-statsguide.gnps2.org/), [Streamlit](https://metabolomics-statistics.streamlit.app/) without installation (recommended for smaller datasets)

### **Disclaimer:**
#### For Code Copying:
- **GitHub Rendering Issues:** GitHub might not display Jupyter notebooks correctly due to file size or complex outputs. For a complete view, download the notebook and open it with Jupyter Notebook/JupyterLab, or access it through the provided Google Colab links mentioned above.
- **Code Transfer:** To copy code into another environment (e.g., RStudio), please use the respective Google Colab or Jupyter viewed version to ensure all content, including HTML in text cells, is accurately transferred. GitHub's rendering limitations might affect some symbols, so following these steps is recommended for optimal compatibility.

#### For GNPS Quickstart Users:
- **Quickstart GNPS 2 Recommendation:** We advise Quickstart GNPS users to switch to the latest Quickstart GNPS 2 for FBMN-STATS and accessing the Notebooks. The previous version of Quickstart GNPS does not generate the reformatted output needed for Notebook/Web app integration, leading to incorrect feature tables. To avoid data retrieval issues, refrain from using the older Quickstart version in GNPS to follow this protocol.

#### For Google Colab Users:
- **Setting Up in Colab:** To use this notebook with your data in Colab, first, save a copy to your Google Drive by selecting **File → Save a copy in Drive**. You can rename the notebook as you see fit. The saved copy will be located in the **'Colab Notebooks'** folder of your Drive.
- **Colab vs. Jupyter Notebook:** While Colab offers a Jupyter Notebook environment, it differs in file loading and output file generation. For specific instructions tailored to Colab users, refer to the detailed guidance below.

## For QIIME2 Users:
[Follow the information on the README file in the QIIME2 folder](https://github.com/Functional-Metabolomics-Lab/FBMN-STATS/tree/main/QIIME2#readme) and for more information, refer to the SI document of the article. Note: The Notebook provided here cannot be accessed using Google Colab.  

## For first time Colab users, some useful information to note:

### 1. Package Installation:
Since Colab does not come pre-installed with R packages (or libraries) when running our R Notebook in Colab, we need to install the packages every time we run the notebook and the installation might take some time. However, direct Jupyter Notebook users need to install it only once as it is installed locally.

### 2. Setting a working directory and loading input files:
![Google-Colab Files Upload](https://github.com//abzer005/Images-for-Jupyter-Notebooks/blob/main/Image_Google_Colab.png?raw=true)
- Unlike Jupyter Notebook, it is not possible to access the files from your local computer in a Google Colab space as it is cloud-based. So we can directly upload the necessary files into the Colab using the <b>'Files icon'</b> on the left corner of your Colab space as shown in the image (a). 
- In order to keep our data organised, we can create a new folder called 'My_TestData' in the Colab space by right clicking on the white space as shown in image (b). We can set this new folder as our working directory.
```
setwd("/My_TestData") 
```
As shown in the image (c), you can then simply upload the files from your local PC to the new folder 'My_TestData' and then continue running the rest of the script.
 
 ### 3. Getting output files from Google Colab:
 
 All the output files will be stored under the working directory. You need to download all the result files from the directory at the end of your session as they are only saved in the Colud and not in your local PC like Jupyter Notebook. You can download the individual files manually by right clicking on each file and downloading it. Else, we can zip the folder and maually download only the zip file.

``` #To zip the folder:
utils::zip(zipfile = 'TestData_Results', files = "/My_TestData/")
```

### 4. Limitations of Google Colab:
Although Colab is easier to use and is all Cloud-based, the main problem with the Colab environment is when you leave the Colab notebook idle for 90 mins or continuously used it for 12 hours, the runtime will automatically disconnect. This means you will lose all your variables, installed packages, and files. Hence, you need to rerun the entire notebook. Another limitation is disk space of 77 GB for the user. Please be aware of this while working with larger datasets and running longer notebooks.
