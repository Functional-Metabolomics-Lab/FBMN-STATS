import streamlit as st
import base64
from src.common import *

page_setup()

st.image("assets/FBMN-STATS-GUIed_logo2.png", use_column_width=True)

st.markdown("""
## Quickstart Guide

Welcome to the FBMN-STATS, a web app implementation of the [statistics notebooks](https://github.com/Functional-Metabolomics-Lab/Statistical-analysis-of-non-targeted-LC-MSMS-data) for metabolomics by the [Functional Metabolomics Lab](https://github.com/Functional-Metabolomics-Lab).
             as part of the article '[The Hitchhiker’s Guide to Statistical Analysis of Feature-based Molecular Networks from Non-Targeted Metabolomics Data](https://doi.org/10.26434/chemrxiv-2023-wwbt0)'. 
            These notebooks are developed by the Virtual Multi Omics Lab ([VMOL](https://vmol.org/)).
            This app facilitates downstream statistical analysis of Feature-Based Molecular Networking data, simplifying the process for researchers.       

### Getting Started
This web app requires two primary inputs: a feature quantification table and metadata table. Users with FBMN Job IDs from GNPS or GNPS2 can easily fetch necessary files by entering the job IDs via the 'Data Preparation' page. 
            This page also offers subsequent data cleanup steps such as Blank Removal, Imputation, and Normalization.

**⚠️ Warning:** Our data cleanup options, including normalization methods like Total Ion Count (TIC) normalization and center-scaling, are selected due to their widespread use. However, we recognize that these methods may not be suitable for all types of data. We encourage users to consider various normalization techniques to best suit their dataset's needs.
            This tool aims to offer a quick results overview and serves primarily for educational purposes. For comprehensive insights into data cleanup methodologies, please refer to our article and the referenced literature.
""")


st.subheader('Data Preparation Essentials')
st.markdown("""
- Required tables: **Quantification** and **Metadata**
- Supported formats include: `tsv`, `txt`, `csv`, and `xlsx`
- Feature tables with an **metabolite** column are indexed accordingly
- Automatic feature indexing available with `m/z`, `RT`, and optional `row ID` columns
- Sample filenames must include `mzML` extensions
- The metadata table must have a `filename` column and can include attribute columns
- Example data available for reference
- Proceed to **Data Cleanup** for blank removal and missing value imputation
""")

st.markdown("""          
Example feature table:  
 
|metabolite|sample1.mzML|sample2.mzML|blank.mzML|
|---|---|---|---|
|1|1000|1100|100|
|2|2000|2200|200|
""")
st.write(' ')
st.markdown("""        
Example meta data table:
            
|filename|Sample_Type|Time_Point|
|---|---|---|
|sample1.mzML|Sample|1h|
|sample2.mzML|Sample|2h|
|blank.mzML|Blank|N/A| 
""")

st.write(' ')
st.subheader('Statistical Analyses Available')
st.markdown("""
- **PCA**
- **Multivariate Analysis:** PERMANOVA & PCoA
- **Hierarchical Clustering & Heatmaps**
- **Univariate Analysis:** ANOVA, Tukey's, Student's t-test, Kruskal-Wallis & Dunn's
""")


st.subheader('Outputs')
st.markdown("""
Generated results include csv tables and images, aiding in data presentation and publication.
""")


st.subheader('Interactive Plots')
st.markdown("""
💡 **All plots are interactive!**
- Select area with your mouse to zoom in
- Double click in the plot to zoom back out
- Save plots using the camera icon in the top right corner (specify image format in settings panel)
""")


st.subheader('Settings Panel')
st.markdown("""
1. **P-value Correction:** These are FDR (False Disovery Rate) corrections applied for multiple univariate tests. Available options include Bonferroni, Sidak, Benjamini-Hochberg (BH), Benjamini-Yekutieli (BY), and an option for no correction, with Bonferroni set as the default.  
            While Bonferroni is known for controlling false positives, it may inadvertently increase false negatives. Advanced methods like BH and BY aim to balance true discoveries against false positives more effectively. We recommend BH for FDR correction to optimize analysis outcomes.
            
    Note that changing the p-value correction settings does not automatically update the corrected p-values. To update results re-run the analysis.

2. **Image Export Format:** Choose from svg, png, jpeg, webp. Recommendations: png for presentations, svg for publications.
""")


st.subheader('Limitations of the App')
st.markdown("""
- Be mindful of the 200 MB data limit. There is a possibility of server slowdowns or crashes with larger datasets. The GUI's simplicity and limited graphical options are designed for introductory purposes and does not allow customization for deeper analysis. 
""")


st.subheader('Citation and Resources')
st.markdown("""
For citations and further resources, please refer to our [article](https://doi.org/10.26434/chemrxiv-2023-wwbt0).
""")


st.subheader("We Value Your Feedback")
st.markdown("""
Your feedback and suggestions are invaluable to us as we strive to enhance this tool. 
            As a small team, we greatly appreciate any contributions you can make. 
            Please feel free to create an issue on our GitHub repository to share your thoughts or report any issues you encounter.

[Create an Issue on GitHub](https://github.com/Functional-Metabolomics-Lab/FBMN-STATS/issues/new)
""")

st.subheader("Functional-Metabolomics-Lab")

c1, c2, c3 = st.columns(3)
c1.markdown(
    """<a href="https://github.com/Functional-Metabolomics-Lab">
    <img src="data:image/png;base64,{}" width="100">
    </a>""".format(
        base64.b64encode(open("./assets/github-logo.png", "rb").read()).decode()
    ),
    unsafe_allow_html=True,
)
c2.markdown(
    """<a href="https://www.youtube.com/@functionalmetabolomics">
    <img src="data:image/png;base64,{}" width="100">
    </a>""".format(
        base64.b64encode(open("./assets/youtube-logo.png", "rb").read()).decode()
    ),
    unsafe_allow_html=True,
)
c3.markdown(
    """<a href="https://twitter.com/func_metabo_lab">
    <img src="data:image/png;base64,{}" width="100">
    </a>""".format(
        base64.b64encode(open("./assets/x-logo.png", "rb").read()).decode()
    ),
    unsafe_allow_html=True,
)

