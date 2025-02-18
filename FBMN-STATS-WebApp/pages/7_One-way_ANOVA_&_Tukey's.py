import streamlit as st
from src.common import *
from src.anova import *


page_setup()

st.markdown("# One-way ANOVA & Tukey's")

with st.expander("📖 About"):
    st.markdown(
        """Analysis of variance (ANOVA) is a statistical method used to compare means between two or more groups. ANOVA tests whether there is a significant difference between the means of different groups based on the variation within and between groups. If ANOVA reveals that there is a significant difference between at least two group means, post hoc tests are used to determine which specific groups differ significantly from one another. Tukey's post hoc test is a widely used statistical method for pairwise comparisons after ANOVA. It accounts for multiple comparisons and adjusts the p-values accordingly, allowing for a more accurate identification of significant group differences."""
    )
    st.image("assets/figures/anova.png")
    st.image("assets/figures/tukeys.png")

if not st.session_state.data.empty:
    c1, c2 = st.columns(2)
    c1.selectbox(
        "attribute for ANOVA test",
        options=[c for c in st.session_state.md.columns if len(set(st.session_state.md[c])) > 1],
        key="anova_attribute",
    )

    c1.button("Run ANOVA", key="run_anova", type="primary")
    if st.session_state.run_anova:
        st.session_state.df_anova = anova(
            st.session_state.data,
            st.session_state.anova_attribute,
            corrections_map[st.session_state.p_value_correction]
        )
        st.rerun()

    if not st.session_state.df_anova.empty:
        attribute_options = list(
            set(st.session_state.md[st.session_state.anova_attribute].dropna())
        )
        attribute_options.sort()

        c2.multiselect(
            "select **two** options for Tukey's comparison",
            options=attribute_options,
            default=attribute_options[:2],
            key="tukey_elements",
            max_selections=2,
            help="Select two options.",
        )
        c2.button(
            "Run Tukey's",
            key="run_tukey",
            type="primary",
            disabled=len(st.session_state.tukey_elements) != 2,
        )
        if st.session_state.run_tukey:
            st.session_state.df_tukey = tukey(
                st.session_state.df_anova,
                st.session_state.anova_attribute,
                st.session_state.tukey_elements,
                corrections_map[st.session_state.p_value_correction]
            )
            st.rerun()

    tab_options = [
        "📈 ANOVA: plot",
        "📁 ANOVA: result table",
        "📊 ANOVA: significant metabolites",
    ]
    if not st.session_state.df_tukey.empty:
        tab_options += ["📈 Tukey's: plot", "📁 Tukey's: result"]

    if not st.session_state.df_anova.empty:
        tabs = st.tabs(tab_options)
        with tabs[0]:
            fig = get_anova_plot(st.session_state.df_anova)
            show_fig(fig, "anova")
        with tabs[1]:
            show_table(st.session_state.df_anova)
        with tabs[2]:
            c1, _ = st.columns(2)
            c1.selectbox(
                "select metabolite",
                sorted(
                    list(
                        st.session_state.df_anova[
                            st.session_state.df_anova["significant"] == True
                        ].index
                    )
                ),
                key="anova_metabolite",
            )

            fig = get_metabolite_boxplot(
                st.session_state.df_anova,
                st.session_state.anova_metabolite,
            )

            show_fig(fig, f"anova-{st.session_state.anova_metabolite}")

        if not st.session_state.df_tukey.empty:
            with tabs[3]:
                fig = get_tukey_volcano_plot(st.session_state.df_tukey)
                show_fig(fig, "tukeys")
            with tabs[4]:
                show_table(st.session_state.df_tukey, "tukeys")

else:
    st.warning(
        "Please complete data clean up step first! (Preparing data for statistical analysis)"
    )
