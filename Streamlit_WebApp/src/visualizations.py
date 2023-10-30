import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np


def get_feature_frequency_fig(df):
    bins, bins_label, a = [-1, 0, 1, 10], ["-1", "0", "1", "10"], 2

    while a <= 10:
        bins_label.append(np.format_float_scientific(10**a))
        bins.append(10**a)
        a += 1

    freq_table = pd.DataFrame(bins_label)
    frequency = pd.DataFrame(
        np.array(
            np.unique(np.digitize(df.to_numpy(), bins, right=True), return_counts=True)
        ).T
    ).set_index(0)
    freq_table = pd.concat([freq_table, frequency], axis=1).fillna(0).drop(0)
    freq_table.columns = ["intensity", "Frequency"]
    freq_table["Log(Frequency)"] = np.log(freq_table["Frequency"] + 1)

    fig = px.bar(
        freq_table,
        x="intensity",
        y="Log(Frequency)",
        template="plotly_white",
        width=600,
        height=400,
    )

    fig.update_traces(marker_color="#696880")
    fig.update_layout(
        font={"color": "grey", "size": 12},
        title={
            "text": "FEATURE INTENSITY - FREQUENCY PLOT",
            "x": 0.5,
            "font_color": "#3E3D53",
        },
    )

    return fig


def get_missing_values_per_feature_fig(df, cutoff_LOD):
    # check the number of missing values per feature in a histogram
    n_zeros = df.T.apply(lambda x: sum(x <= cutoff_LOD))

    fig = px.histogram(n_zeros, template="plotly_white", width=600, height=400)

    fig.update_traces(marker_color="#696880")
    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={"text": "MISSING VALUES PER FEATURE", "x": 0.5, "font_color": "#3E3D53"},
        xaxis_title="number of missing values",
        yaxis_title="count",
        showlegend=False,
    )
    return fig


def get_anova_plot(anova):
    # first plot insignificant features
    fig = px.scatter(
        x=anova[anova["significant"] == False]["F"].apply(np.log),
        y=anova[anova["significant"] == False]["p"].apply(lambda x: -np.log(x)),
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
        text=anova["metabolite"].iloc[:5],
        textposition="top left",
        textfont=dict(color="#ef553b", size=12),
        name="significant",
    )

    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={
            "text": "ANOVA - FEATURE SIGNIFICANCE",
            "x": 0.5,
            "font_color": "#3E3D53",
        },
        xaxis_title="log(F)",
        yaxis_title="-log(p)",
        showlegend=False,
    )
    return fig


def get_tukey_volcano_plot(tukey):
    # create figure
    fig = px.scatter(template="plotly_white")

    # plot insignificant values
    fig.add_trace(
        go.Scatter(
            x=tukey[tukey["stats_significant"] == False]["stats_diff"],
            y=tukey[tukey["stats_significant"] == False]["stats_p"].apply(
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
            x=tukey[tukey["stats_significant"]]["stats_diff"],
            y=tukey[tukey["stats_significant"]]["stats_p"].apply(lambda x: -np.log(x)),
            mode="markers+text",
            text=tukey["stats_metabolite"].iloc[:5],
            textposition="top right",
            textfont=dict(color="#ef553b", size=12),
            marker_color="#ef553b",
            name="significant",
        )
    )

    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={"text": "TUKEY - FEATURE DIFFERENCE", "x": 0.5, "font_color": "#3E3D53"},
        xaxis_title="stats_diff",
        yaxis_title="-log(p)",
    )
    return fig


def get_metabolite_boxplot(anova, data, metabolite, attribute):
    p_value = anova.set_index("metabolite")._get_value(metabolite, "p")
    df = data[[attribute, metabolite]]
    title = f"{metabolite}<br>p-value: {p_value}"
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
        title={"text": title, "x": 0.5, "font_color": "#3E3D53"},
        xaxis_title=attribute.replace("ATTRIBUTE_", ""),
        yaxis_title="intensity scales and centered",
    )
    return fig


def get_pca_scatter_plot(pca_df, pca, attribute, md):
    title = f"PRINCIPLE COMPONENT ANALYSIS"

    df = pd.merge(
        pca_df[["PC1", "PC2"]],
        md[attribute].apply(str),
        left_index=True,
        right_index=True,
    )
    import streamlit as st

    st.dataframe(df)
    fig = px.scatter(
        df,
        x="PC1",
        y="PC2",
        template="plotly_white",
        width=600,
        height=400,
        color=attribute,
        hover_name=df.index,
    )

    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={"text": title, "x": 0.2, "font_color": "#3E3D53"},
        xaxis_title=f"PC1 {round(pca.explained_variance_ratio_[0]*100, 1)}%",
        yaxis_title=f"PC2 {round(pca.explained_variance_ratio_[1]*100, 1)}%",
    )
    return fig


def get_pca_scree_plot(pca_df, pca):
    # To get a scree plot showing the variance of each PC in percentage:
    percent_variance = np.round(pca.explained_variance_ratio_ * 100, decimals=2)

    fig = px.bar(
        x=pca_df.columns,
        y=percent_variance,
        template="plotly_white",
        width=500,
        height=400,
    )
    fig.update_traces(marker_color="#696880", width=0.5)
    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={"text": "PCA - VARIANCE", "x": 0.5, "font_color": "#3E3D53"},
        xaxis_title="principal component",
        yaxis_title="variance (%)",
    )
    return fig

    #   st.plotly_chart(get_pcoa_scatter_plot(st.session_state.pcoa_result, st.session_state.md, attribute))


def get_pcoa_scatter_plot(pcoa, md_samples, attribute):
    df = pcoa.samples[["PC1", "PC2"]]
    df = df.set_index(md_samples.index)
    df = pd.merge(
        df[["PC1", "PC2"]],
        md_samples[attribute].apply(str),
        left_index=True,
        right_index=True,
    )

    title = f"PRINCIPLE COORDINATE ANALYSIS"
    fig = px.scatter(
        df,
        x="PC1",
        y="PC2",
        template="plotly_white",
        width=600,
        height=400,
        color=attribute,
        hover_name=df.index,
    )

    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={"text": title, "x": 0.18, "font_color": "#3E3D53"},
        xaxis_title=f"PC1 {round(pcoa.proportion_explained[0]*100, 1)}%",
        yaxis_title=f"PC2 {round(pcoa.proportion_explained[1]*100, 1)}%",
    )
    return fig


def get_pcoa_variance_plot(pcoa):
    # To get a scree plot showing the variance of each PC in percentage:
    percent_variance = np.round(pcoa.proportion_explained * 100, decimals=2)

    fig = px.bar(
        x=[f"PC{x}" for x in range(1, len(pcoa.proportion_explained) + 1)],
        y=percent_variance,
        template="plotly_white",
        width=500,
        height=400,
    )
    fig.update_traces(marker_color="#696880", width=0.5)
    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={"text": "PCoA - VARIANCE", "x": 0.5, "font_color": "#3E3D53"},
        xaxis_title="principal component",
        yaxis_title="variance (%)",
    )
    return fig


def get_dendrogram(scaled, label_pos="bottom"):
    fig = ff.create_dendrogram(scaled, labels=list(scaled.index))
    fig.update_layout(template="plotly_white")
    fig.update_xaxes(side=label_pos)
    return fig


def get_heatmap(ord_ft):
    # Heatmap
    fig = px.imshow(
        ord_ft,
        y=list(ord_ft.index),
        x=list(ord_ft.columns),
        text_auto=True,
        aspect="auto",
        color_continuous_scale="PuOr_r",
        range_color=[-3, 3],
    )

    fig.update_layout(
        autosize=False, width=700, height=1200, xaxis_title="", yaxis_title=""
    )

    # fig.update_yaxes(visible=False)
    fig.update_xaxes(tickangle=35)
    return fig
