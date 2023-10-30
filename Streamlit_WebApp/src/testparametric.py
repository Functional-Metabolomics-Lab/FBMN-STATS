import streamlit as st
import pandas as pd
import plotly.express as px
import scipy.stats as stats


@st.cache_data
def test_equal_variance(attribute, between):
    # test for equal variance
    data = pd.concat([st.session_state.data, st.session_state.md], axis=1)
    variance = pd.DataFrame(
        {
            f"{between[0]} - {between[1]}": [
                stats.levene(
                    data.loc[
                        (data[attribute] == between[0]),
                        f,
                    ],
                    data.loc[
                        (data[attribute] == between[1]),
                        f,
                    ],
                )[1]
                for f in st.session_state.data.columns
            ]
        }
    )
    fig = px.histogram(
        variance,
        nbins=100,
        template="plotly_white",
    )
    fig.update_traces(marker_color="#696880")
    fig.update_layout(
        bargap=0.2,
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={"text": f"TEST FOR EQUAL VARIANCE", "font_color": "#3E3D53"},
        xaxis_title="p-value",
        yaxis_title="count",
        showlegend=False
    )
    return fig


@st.cache_data
def test_normal_distribution(attribute, between):
    # test for normal distribution
    data = pd.concat([st.session_state.data, st.session_state.md], axis=1)
    for b in between:
        if st.session_state.md[attribute].value_counts().loc[b] < 3:
            st.warning("You need at least 3 values in each option to test for normality!")
            return None
    normality = pd.DataFrame(
        {
            f"{b}": [
                stats.shapiro(
                    data.loc[
                        (data[attribute] == between[0]),
                        f,
                    ]
                )[1]
                for f in st.session_state.data.columns
            ]
            for b in between
        }
    )

    fig = px.histogram(
        normality.iloc[:, 1],
        nbins=100,
        template="plotly_white",
        color_discrete_sequence=["#696880", "#ef553b"],
        opacity=0.8,
    )
    fig.update_traces(marker_color="#696880")

    fig.update_layout(
        bargap=0.2,
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={"text": f"TEST FOR NORMALITY", "font_color": "#3E3D53"},
        xaxis_title="p-value",
        yaxis_title="count",
        showlegend=False
    )
    return fig
