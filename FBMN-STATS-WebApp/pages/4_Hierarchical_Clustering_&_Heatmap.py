import streamlit as st
from src.common import *
from src.clustering import *

page_setup()

st.markdown("# Hierarchical Clustering & Heatmap")

with st.expander("📖 About"):
    st.markdown(
        """
Hierarchical clustering analysis (HCA) is a popular unsupervised technique used for grouping data points based on their similarities. In this method, the data is organized in a tree-like structure or dendrogram, where each branch represents a cluster of data points with similar features. The clustering process starts with each data point being considered as a separate cluster, and then iteratively combines similar clusters until all the data points are in a single cluster.

The clustering relies on a distance matrix 'distm', calculated from the feature quantification table (submitted during the data preparation stage), using a specific distance metric  (e.g., Euclidean, Canberra). By default, we use Euclidean distance. Another important factor is the linkage method, which measures the distance between these clusters (e.g., complete, single, average). Our default choice uses the 'complete' method, it calculates the maximum distance between clusters before merging them. Currently, users do not have the option to adjust the distance metric or linkage method. Following HCA, a dendrogram is produced, showing the distances (or 'heights') at which clusters merge or split along the y-axis. The dendrogram offers insights into the clustering process and the relationships between data points. There are a lot of [good videos](https://www.youtube.com/watch?v=7xHsRkOdVwo) and resources out there explaining very well the principle behind clustering. 

Complementing the dendrogram, heatmaps provide a color-coded representation of data, showcasing trends of each feature across samples. Heatmaps are particularly useful for analyzing large datasets with complex relationships between features. The heatmap provides an easy-to-read visualization of the similarities and differences between the data points (features) and clusters, with similar data points appearing as blocks of similar colors, suggesting functional relationships between features and sample. 

The dataset used for both HCA and heatmap is the data submitted for statistics from the ‘Data preparation stage’. Similarly, the downloadable table in this section corresponds to the same dataset submitted for statistical analysis. While current settings for HCA parameters are fixed to defaults, these tools (HCA and heatmaps) still offer valuable insights into the dataset's inherent clustering and variable relationships.
"""
    )
    st.image("assets/figures/clustering.png")

if not st.session_state.data.empty:
    t1, t2, t3 = st.tabs(["📈 Clustering", "📊 Heatmap", "📁 Heatmap Data"])
    with t1:
        fig = get_dendrogram(st.session_state.data, "bottom")
        show_fig(fig, "clustering")
    fig, df = get_heatmap(st.session_state.data)
    with t2:

        show_fig(fig, "heatmap")
    with t3:
        show_table(df, "heatmap-data")
else:
    st.warning("Please complete data preparation step first!")