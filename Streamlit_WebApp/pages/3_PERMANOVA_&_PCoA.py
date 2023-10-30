import streamlit as st
from src.common import *
from src.pcoa import *

page_setup()

st.markdown("# Multivariate Statistics")
st.markdown("### PERMANOVA & Principle Coordinate Analysis (PCoA)")

with st.expander("📖 About"):
    st.markdown(
        """
PERMANOVA (Permutational Multivariate Analysis of Variance) is a statistical method used to test differences in multivariate data between two or more groups. It is similar to traditional ANOVA but accounts for correlations between variables and allows for the testing of non-parametric data. It works by permuting the data to create a null distribution, which is then used to calculate a p-value for the observed differences between groups.

Principal Coordinate Analysis (PCoA) is a multivariate technique used to analyze the structure of a distance matrix. PCoA transforms the distance matrix into a set of orthogonal axes that capture the maximum variation in the data. It is a useful tool for visualizing and exploring patterns in multivariate data, particularly in environmental and ecological research.

This [video tutorial](https://www.youtube.com/watch?v=GEn-_dAyYME) by StatQuest summarizes nicely the basic principles of PCoA. 
"""
    )
    st.image("assets/figures/pcoa.png")


if not st.session_state.data.empty:
    c1, c2 = st.columns(2)
    c1.selectbox(
        "attribute for multivariate analysis",
        [c for c in st.session_state.md.columns if len(set(st.session_state.md[c])) > 1 and len(set(st.session_state.md[c])) != st.session_state.md.shape[0]],
        key="pcoa_attribute",
    )
    c2.selectbox(
        "distance matrix",
        [
            "canberra",
            "chebyshev",
            "correlation",
            "cosine",
            "euclidean",
            "hamming",
            "jaccard",
            "matching",
            "minkowski",
            "seuclidean",
        ],
        key="pcoa_distance_matrix",
    )
    permanova, pcoa_result = permanova_pcoa(
        st.session_state.data,
        st.session_state.pcoa_distance_matrix,
        st.session_state.md[st.session_state.pcoa_attribute],
    )

    if not permanova.empty:
        t1, t2, t3 = st.tabs(
            [
                "📁 PERMANOVA statistics",
                "📈 Principle Coordinate Analysis",
                "📊 Explained variance",
            ]
        )
        with t1:
            show_table(permanova, "PERMANOVA-statistics")
        with t2:
            fig = get_pcoa_scatter_plot(
                pcoa_result,
                st.session_state.md,
                st.session_state.pcoa_attribute,
            )
            show_fig(fig, "principle-coordinate-analysis")
        with t3:
            fig = get_pcoa_variance_plot(pcoa_result)
            show_fig(fig, "pcoa-variance")

else:
    st.warning("Please complete data preparation step first!")
