import streamlit as st
from src.common import *
from src.kruskal import *


page_setup()

st.markdown("# Kruskal Wallis & Dunn's post hoc")

with st.expander("📖 About"):
    st.markdown(
        """The Kruskal-Wallis test helps determine if there are significant differences among multiple groups, and if significant differences exist, Dunn's post hoc test helps pinpoint which specific groups differ from each other. These non-parametric tests are valuable tools for analyzing data when the assumptions of parametric tests are not met or when working with ordinal or skewed data."""
    )
    st.image("assets/figures/kruskal-wallis.png")
    st.image("assets/figures/dunn.png")

if not st.session_state.data.empty:
    c1, c2 = st.columns(2)
    c1.selectbox(
        "attribute for Kruskal Wallis test",
        options=[c for c in st.session_state.md.columns if len(set(st.session_state.md[c])) > 1],
        key="kruskal_attribute",
    )

    c1.button("Run Kruskal Wallis", key="run_kruskal", type="primary")
    if st.session_state.run_kruskal:
        st.session_state.df_kruskal = kruskal_wallis(
            st.session_state.data, st.session_state.kruskal_attribute,
            corrections_map[st.session_state.p_value_correction]
        )
        st.rerun()

    if not st.session_state.df_kruskal.empty:
        if any(st.session_state.df_kruskal["significant"]):
            attribute_options = list(
                set(st.session_state.md[st.session_state.kruskal_attribute].dropna())
            )
            attribute_options.sort()

            c2.multiselect(
                "select **two** options for Dunn's comparison",
                options=attribute_options,
                default=attribute_options[:2],
                key="dunn_elements",
                max_selections=2,
                help="Select two options.",
            )
            c2.button(
                "Run Dunn's",
                key="run_dunn",
                type="primary",
                disabled=len(st.session_state.dunn_elements) != 2,
            )
            if st.session_state.run_dunn:
                st.session_state.df_dunn = dunn(
                    st.session_state.df_kruskal,
                    st.session_state.kruskal_attribute,
                    st.session_state.dunn_elements,
                    corrections_map[st.session_state.p_value_correction]
                )
                st.rerun()
        else:
            st.warning("No significant metabolites found in Kruskal Wallis test after p-value correction.")

    tab_options = [
        "📈 Kruskal Wallis: plot",
        "📁 Kruskal Wallis: result table",
        "📊 Kruskal Wallis: significant metabolites",
    ]
    if not st.session_state.df_dunn.empty:
        tab_options += ["📁 Dunn's: result"]

    if not st.session_state.df_kruskal.empty:
        tabs = st.tabs(tab_options)
        with tabs[0]:
            fig = get_kruskal_plot(st.session_state.df_kruskal)
            show_fig(fig, "kruskal")
        with tabs[1]:
            show_table(st.session_state.df_kruskal)
        with tabs[2]:
            c1, _ = st.columns(2)
            c1.selectbox(
                "select metabolite",
                sorted(
                    list(
                        st.session_state.df_kruskal["metabolite"][
                            st.session_state.df_kruskal["significant"] == True
                        ]
                    )
                ),
                key="kruskal_metabolite",
            )
            if st.session_state.kruskal_metabolite:
                fig = get_metabolite_boxplot(
                    st.session_state.df_kruskal,
                    st.session_state.kruskal_metabolite,
                )
                show_fig(fig, f"kruskal-{st.session_state.kruskal_metabolite}")

        if not st.session_state.df_dunn.empty:
            with tabs[3]:
                show_table(st.session_state.df_dunn, "dunns")

else:
    st.warning(
        "Please complete data clean up step first! (Preparing data for statistical analysis)"
    )
