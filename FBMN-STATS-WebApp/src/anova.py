import streamlit as st
import pandas as pd
import numpy as np
import pingouin as pg
import plotly.express as px
import plotly.graph_objects as go


def gen_anova_data(df, columns, groups_col):
    for col in columns:
        result = pg.anova(data=df, dv=col, between=groups_col, detailed=True).set_index(
            "Source"
        )
        p = result.loc[groups_col, "p-unc"]
        f = result.loc[groups_col, "F"]
        yield col, p, f


def add_p_correction_to_anova(df, correction):
    # add Bonferroni corrected p-values for multiple testing correction
    if "p-corrected" not in df.columns:
        df.insert(2, "p-corrected",
                  pg.multicomp(df["p"].astype(float), method=correction)[1])
    # add significance
    if "significant" not in df.columns:
        df.insert(3, "significant", df["p-corrected"] < 0.05)
    # sort by p-value
    df.sort_values("p", inplace=True)
    return df


@st.cache_data
def anova(df, attribute, correction):
    df = pd.DataFrame(
        np.fromiter(
            gen_anova_data(
                pd.concat([df, st.session_state.md], axis=1),
                df.columns,
                attribute,
            ),
            dtype=[("metabolite", "U100"), ("p", "f"), ("F", "f")],
        )
    )
    df = df.dropna()
    df = add_p_correction_to_anova(df, correction)
    return df.set_index("metabolite")


@st.cache_resource
def get_anova_plot(anova):
    # first plot insignificant features
    fig = px.scatter(
        x=anova[anova["significant"] == False]["F"].apply(np.log),
        y=anova[anova["significant"] == False]["p"].apply(
            lambda x: -np.log(x)),
        template="plotly_white",
        width=600,
        height=600,
    )
    fig.update_traces(marker_color="#696880")

    # plot significant features
    fig.add_scatter(
        x=anova[anova["significant"]]["F"].apply(np.log),
        y=anova[anova["significant"]]["p"].apply(lambda x: -np.log(x)),
        mode="markers+text",
        text=anova.index[:6],
        textposition="top left",
        textfont=dict(color="#ef553b", size=14),
        name="significant",
    )

    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={
            "text": f"ANOVA - {st.session_state.anova_attribute.upper()}",
            "font_color": "#3E3D53"
        },
        xaxis_title="log(F)",
        yaxis_title="-log(p)",
        showlegend=False
    )
    fig.update_yaxes(title_standoff=10)
  
    # fig.update_yaxes(title_font_size=20)
    # fig.update_xaxes(title_font_size=20)

    return fig


@st.cache_resource
def get_metabolite_boxplot(anova, metabolite):
    attribute = st.session_state.anova_attribute
    p_value = anova.loc[metabolite, "p-corrected"]
    df = pd.concat([st.session_state.data, st.session_state.md], axis=1)[
        [attribute, metabolite]
    ]
    title = f"{metabolite}<br>corrected p-value: {str(p_value)[:6]}"
    fig = px.box(
        df,
        x=attribute,
        y=metabolite,
        template="plotly_white",
        width=800,
        height=600,
        points="all",
        color=attribute,
    )

    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={"text": title, "font_color": "#3E3D53"},
        xaxis_title=attribute,
        yaxis_title="intensity",
    )
    return fig


def gen_pairwise_tukey(df, metabolites, attribute):
    """Yield results for pairwise Tukey test for all metabolites between two options within the attribute."""
    for metabolite in metabolites:
        tukey = pg.pairwise_tukey(df, dv=metabolite, between=attribute)
        yield (
            metabolite,
            tukey.loc[0, "diff"],
            tukey.loc[0, "p-tukey"],
            attribute,
            tukey.loc[0, "A"],
            tukey.loc[0, "B"],
            tukey.loc[0, "mean(A)"],
            tukey.loc[0, "mean(B)"],
        )


def add_p_value_correction_to_tukeys(tukey, correction):
    if "p-corrected" not in tukey.columns:
        # add Bonferroni corrected p-values
        tukey.insert(
            3, "p-corrected", pg.multicomp(
                tukey["stats_p"].astype(float), method=correction)[1]
        )
        # add significance
        tukey.insert(4, "stats_significant", tukey["p-corrected"] < 0.05)
        # sort by p-value
        tukey.sort_values("stats_p", inplace=True)
    return tukey


@st.cache_data
def tukey(df, attribute, elements, correction):
    significant_metabolites = df[df["significant"]].index
    data = pd.concat(
        [
            st.session_state.data.loc[:, significant_metabolites],
            st.session_state.md.loc[:, attribute],
        ],
        axis=1,
    )
    data = data[data[attribute].isin(elements)]
    tukey = pd.DataFrame(
        np.fromiter(
            gen_pairwise_tukey(data, significant_metabolites, attribute),
            dtype=[
                ("stats_metabolite", "U100"),
                (f"diff", "f"),
                ("stats_p", "f"),
                ("attribute", "U100"),
                ("A", "U100"),
                ("B", "U100"),
                ("mean(A)", "f"),
                ("mean(B)", "f"),
            ],
        )
    )
    tukey = tukey.dropna()
    tukey = add_p_value_correction_to_tukeys(tukey, correction)
    return tukey


@st.cache_resource
def get_tukey_volcano_plot(df):
    # create figure
    fig = px.scatter(template="plotly_white")

    # plot insignificant values
    fig.add_trace(
        go.Scatter(
            x=df[df["stats_significant"] == False]["diff"],
            y=df[df["stats_significant"] == False]["stats_p"].apply(
                lambda x: -np.log(x)
            ),
            mode="markers",
            marker_color="#696880",
            name="insignificant",
        )
    )

    # plot significant values
    fig.add_trace(
        go.Scatter(
            x=df[df["stats_significant"]]["diff"],
            y=df[df["stats_significant"]]["stats_p"].apply(
                lambda x: -np.log(x)),
            mode="markers+text",
            text=df["stats_metabolite"].iloc[:5],
            textposition="top right",
            textfont=dict(color="#ef553b", size=12),
            marker_color="#ef553b",
            name="significant",
        )
    )

    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={
            "text": f"TUKEY - {st.session_state.anova_attribute.upper()}: {st.session_state.tukey_elements[0]} - {st.session_state.tukey_elements[1]}",
            "font_color": "#3E3D53",
        },
        xaxis_title=f"diff",
        yaxis_title="-log(p)",
    )
    return fig
