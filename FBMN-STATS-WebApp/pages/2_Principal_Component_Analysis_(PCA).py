import streamlit as st
from src.common import *
from src.pca import *

page_setup()

# pd.concat([st.session_state.md, st.session_state.data], axis=1)

st.markdown("# Principal Component Analysis (PCA)")

with st.expander("📖 About"):
    st.markdown(
        "Principal Component Analysis (PCA) is a statistical method used for dimensionality reduction in multivariate data analysis. It involves transforming a set of correlated variables into a smaller set of uncorrelated variables, known as principal components. These principal components are ordered by their ability to explain the variability in the data, with the first component accounting for the highest amount of variance. PCA can be used to simplify complex data sets, identify patterns and relationships among variables, and remove noise or redundancy from data."
    )
if not st.session_state.data.empty:
    c1, c2 = st.columns(2)
    c1.number_input(
        "number of components",
        2,
        st.session_state.data.shape[0],
        2,
        key="n_components",
    )
    c2.selectbox(
        "attribute for PCA plot", st.session_state.md.columns, key="pca_attribute"
    )
    pca_variance, pca_df = get_pca_df(
        st.session_state.data, st.session_state.n_components
    )

    t1, t2, t3 = st.tabs(["📈 PCA Plot", "📊 Explained variance", "📁 Data"])
    with t1:
        fig = get_pca_scatter_plot(
            pca_df, pca_variance, st.session_state.pca_attribute, st.session_state.md
        )
        show_fig(fig, "principal-component-analysis")
    with t2:
        fig = get_pca_scree_plot(pca_df, pca_variance)
        show_fig(fig, "pca-variance")

    with t3:
        show_table(pca_df, "priciple-components")
else:
    st.warning("Please complete data preparation step first!")
