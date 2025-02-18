import streamlit as st

from src.common import *
from src.testparametric import *

page_setup()

st.markdown("# Parametric assumptions evaluation")
st.markdown("## Normal distribution and equal variance")

with st.expander("📖 Why is this important?"):
    st.markdown(
        "When analyzing data, it is important to choose the appropriate statistical test to use. One of the factors to consider is whether the data follows a normal distribution and has equal variance. This is because many statistical tests assume that the data is normally distributed and has equal variance. If the data violates these assumptions, parametric tests may not be appropriate and non-parametric tests should be used instead. In this context, testing for normal distribution and equal variance is crucial in determining the most suitable statistical test for the analysis."
    )

if not st.session_state.data.empty:
    c1, c2 = st.columns(2)
    c1.selectbox(
        "select attribute of interest",
        options=[c for c in st.session_state.md.columns if len(set(st.session_state.md[c])) > 1],
        key="test_attribute",
    )
    attribute_options = list(
        set(st.session_state.md[st.session_state.test_attribute].dropna())
    )
    attribute_options.sort()
    c2.multiselect(
        "select **two** options from the attribute for comparison",
        options=attribute_options,
        default=attribute_options[:2],
        key="test_options",
        max_selections=2,
        help="Select two options.",
    )
    if st.session_state.test_attribute and len(st.session_state.test_options) == 2:
        tabs = st.tabs(["📊 Normal distribution (Shapiro-Wilk test)", "📊 Equal variance (Levene test)"])
        with tabs[0]:
            fig = test_normal_distribution(st.session_state.test_attribute, st.session_state.test_options, corrections_map[st.session_state.p_value_correction])
            if fig:
                show_fig(fig, "test-normal-distribution")
        with tabs[1]:
            fig = test_equal_variance(st.session_state.test_attribute, st.session_state.test_options, corrections_map[st.session_state.p_value_correction])
            show_fig(fig, "test-equal-variance")

    st.info(
        """💡 **Interpretation**

In both tests low p-values indicate that data points for a feature are **NOT** normal distributed or have similar variance.
To meet **parametric** criteria the p-values in the histograms should not be smaller than 0.05.
When a larger number of data points indicate low p-values, it would be advisable to opt for a **non-parametric** statistical test.
"""
    )
    st.image("assets/figures/decision.png")
else:
    st.warning("Please complete data preparation step first!")
