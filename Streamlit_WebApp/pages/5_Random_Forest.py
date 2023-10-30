import streamlit as st
from src.common import *
from src.randomforest import *

page_setup()

st.title("Random Forest")

with st.expander("📖 About"):
    st.markdown(
        """Get the most important features explaining the selected attribute with supervised learning via random forest model."""
    )
    st.image("assets/figures/random-forest.png")

if not st.session_state.data.empty:
    c1, c2 = st.columns(2)
    c1.selectbox(
        "attribute for supervised learning feature classification",
        options=[c for c in st.session_state.md.columns if len(set(st.session_state.md[c])) > 1],
        key="rf_attribute",
    )
    c2.number_input("number of trees", 1, 500, 100, 50,
                    key = "rf_n_trees",
                    help="number of trees for random forest, check the OOB error plot and select a number of trees where the error rate is low and flat")
    
    if c2.button("Run supervised learning", type="primary"):
        st.session_state.df_oob, st.session_state.df_important_features = run_random_forest(st.session_state.rf_attribute, st.session_state.rf_n_trees)

if not st.session_state.df_important_features.empty:
    tabs = st.tabs(["📈 Analyze optimum number of trees", "📁 Feature ranked by importance"])
    with tabs[0]:
        fig = get_oob_fig(st.session_state.df_oob)
        show_fig(fig, "oob-error")
    with tabs[1]:
        show_table(st.session_state.df_important_features)