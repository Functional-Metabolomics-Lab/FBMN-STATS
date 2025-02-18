import streamlit as st
import pandas as pd
import pingouin as pg
import plotly.express as px
import numpy as np


@st.cache_data
def gen_ttest_data(ttest_attribute, target_groups, paired, alternative, correction, p_correction):
    df = pd.concat([st.session_state.data, st.session_state.md], axis=1)
    ttest = []
    for col in st.session_state.data.columns:
        group1 = df[col][df[ttest_attribute] == target_groups[0]]
        group2 = df[col][df[ttest_attribute] == target_groups[1]]
        result = pg.ttest(group1, group2, paired, alternative, correction)
        result["metabolite"] = col

        ttest.append(result)

    ttest = pd.concat(ttest).set_index("metabolite")
    ttest = ttest.dropna()

    ttest.insert(8, "p-corrected", pg.multicomp(ttest["p-val"].astype(float), method=p_correction)[1])
    # add significance
    ttest.insert(9, "significance", ttest["p-corrected"] < 0.05)
    ttest.insert(10, "st.session_state.ttest_attribute", ttest_attribute)
    ttest.insert(11, "A", target_groups[0])
    ttest.insert(12, "B", target_groups[1])

    return ttest.sort_values("p-corrected")


@st.cache_resource
def plot_ttest(df):
    fig = px.scatter(
        x=df["T"],
        y=df["p-corrected"].apply(lambda x: -np.log(x)),
        template="plotly_white",
        width=600,
        height=600,
        color=df["significance"].apply(lambda x: str(x)),
        color_discrete_sequence=["#ef553b", "#696880"],
        hover_name=df.index,
    )
    
    xlim = [df["T"].min(), df["T"].max()]
    x_padding = abs(xlim[1]-xlim[0])/5
    fig.update_layout(xaxis=dict(range=[xlim[0]-x_padding, xlim[1]+x_padding]))

    r = df["significance"].sum()
    if r > 5:
        r = 5
    for i in range(r):
        fig.add_annotation(
            x=df["T"][i] + (xlim[1] - xlim[0])/12,  # x-coordinate of the annotation
            y=df["p-corrected"].apply(lambda x: -np.log(x))[
                i
            ],  # y-coordinate of the annotation
            text=df.index[i],  # text to be displayed
            showarrow=False,  # don't display an arrow pointing to the annotation
            font=dict(size=10, color="#ef553b"),  # font size of the text
        )

    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={
            "text": f"t-test - FEATURE SIGNIFICANCE - {df.iloc[0, 10].upper()}: {df.iloc[0, 11]} - {df.iloc[0, 12]}",
            "font_color": "#3E3D53",
        },
        xaxis_title="T",
        yaxis_title="-Log(p)",
        showlegend=False,
    )
    return fig


@st.cache_resource
def ttest_boxplot(df_ttest, metabolite):
    df = pd.concat([st.session_state.md, st.session_state.data], axis=1)
    df1 = pd.DataFrame(
        {
            metabolite: df[df[st.session_state.ttest_attribute] == st.session_state.ttest_options[0]].loc[:, metabolite],
            "option": st.session_state.ttest_options[0],
        }
    )
    df2 = pd.DataFrame(
        {
            metabolite: df[df[st.session_state.ttest_attribute] == st.session_state.ttest_options[1]].loc[:, metabolite],
            "option": st.session_state.ttest_options[1],
        }
    )
    df = pd.concat([df1, df2])
    fig = px.box(
        df,
        x="option",
        y=metabolite,
        color="option",
        width=350,
        height=400,
        points="all",
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title=st.session_state.ttest_attribute.replace("st.session_state.ttest_attribute_", ""),
        yaxis_title="intensity",
        template="plotly_white",
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={
            "text": metabolite,
            "font_color": "#3E3D53",
        },
    )
    fig.update_yaxes(title_standoff=10)
    pvalue = df_ttest.loc[metabolite, "p-corrected"]
    if pvalue >= 0.05:
        symbol = "ns"
    elif pvalue >= 0.01:
        symbol = "*"
    elif pvalue >= 0.001:
        symbol = "**"
    else:
        symbol = "***"

    top_y = max(df[metabolite]) * 1.2

    if isinstance(df["option"][0], str) and isinstance(df["option"][1], str):
        x0, x1 = 0, 1
    else:
        x0, x1 = st.session_state.ttest_options[0], st.session_state.ttest_options[1]
    # horizontal line
    fig.add_shape(
        type="line",
        x0=x0,
        y0=top_y,
        x1=x1,
        y1=top_y,
        line=dict(width=1, color="#000000"),
    )
    if symbol == "ns":
        y_margin = max(df[metabolite]) * 0.05
    else:
        y_margin = max(df[metabolite]) * 0.1
    fig.add_annotation(
        x=(x1-x0)/2,
        y=top_y + y_margin,
        text=f"<b>{symbol}</b>",
        showarrow=False,
        font_color="#555555",
    )
    return fig
