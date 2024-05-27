import streamlit as st
import pandas as pd
import io
import uuid
import base64

dataframe_names = ("md",
                   "data",
                   "df_anova",
                   "df_tukey",
                   "df_ttest",
                   "df_kruskal",
                   "df_dunn",
                   "df_important_features",
                   "df_oob",
                   "ft_gnps",
                   "md_gnps",
                   "df_gnps_annotations")

corrections_map = {"Bonferroni": "bonf",
                   "Sidak": "sidak",
                   "Benjamini/Hochberg FDR": "fdr_bh",
                   "Benjamini/Yekutieli FDR": "fdr_by",
                   "no correction": "none"}


def reset_dataframes():
    for key in dataframe_names:
        st.session_state[key] = pd.DataFrame()


def page_setup():
    # streamlit configs
    st.set_page_config(
        page_title="Statistics for Metabolomics",
        page_icon="assets/icon.png",
        # layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )
    # initialize global session state variables if not already present
    # DataFrames
    for key in dataframe_names:
        if key not in st.session_state:
            st.session_state[key] = pd.DataFrame()
    if "data_preparation_done" not in st.session_state:
        st.session_state["data_preparation_done"] = False

    with st.sidebar:
        with st.expander("⚙️ Settings", expanded=True):
            st.selectbox("p-value correction",
                         corrections_map.keys(),
                         key="p_value_correction")
            st.selectbox(
                "image export format",
                ["svg", "png", "jpeg", "webp"],
                key="image_format",
            )
        v_space(1)
        st.image("assets/FBMN-STATS-GUIed_logo2.png", use_column_width=True)
        v_space(1)
        st.image("assets/vmol-icon.png", use_column_width=True) 
        v_space(1)
        st.markdown("## Functional-Metabolomics-Lab")
        c1, c2, c3 = st.columns(3)
        c1.markdown(
            """<a href="https://github.com/Functional-Metabolomics-Lab">
            <img src="data:image/png;base64,{}" width="50">
            </a>""".format(
                base64.b64encode(open("./assets/github-logo.png", "rb").read()).decode()
            ),
            unsafe_allow_html=True,
        )
        c2.markdown(
            """<a href="https://www.youtube.com/@functionalmetabolomics">
            <img src="data:image/png;base64,{}" width="50">
            </a>""".format(
                base64.b64encode(open("./assets/youtube-logo.png", "rb").read()).decode()
            ),
            unsafe_allow_html=True,
        )
        c3.markdown(
            """<a href="https://twitter.com/func_metabo_lab">
            <img src="data:image/png;base64,{}" width="50">
            </a>""".format(
                base64.b64encode(open("./assets/x-logo.png", "rb").read()).decode()
            ),
            unsafe_allow_html=True
        )


def v_space(n, col=None):
    for _ in range(n):
        if col:
            col.write("")
        else:
            st.write("")


def open_df(file):
    separators = {"txt": "\t", "tsv": "\t", "csv": ","}
    try:
        if type(file) == str:
            ext = file.split(".")[-1]
            if ext != "xlsx":
                df = pd.read_csv(file, sep=separators[ext])
            else:
                df = pd.read_excel(file)
        else:
            ext = file.name.split(".")[-1]
            if ext != "xlsx":
                df = pd.read_csv(file, sep=separators[ext])
            else:
                df = pd.read_excel(file)
        # sometimes dataframes get saved with unnamed index, that needs to be removed
        if "Unnamed: 0" in df.columns:
            df.drop("Unnamed: 0", inplace=True, axis=1)
        return df
    except:
        return pd.DataFrame()


def show_table(df, title="", col="", download=True):
    if col:
        col = col
    else:
        col = st
    col.dataframe(df, use_container_width=True)


def show_fig(fig, download_name, container_width=True):
    st.plotly_chart(
        fig,
        use_container_width=container_width,
        config={
            "displaylogo": False,
            "modeBarButtonsToRemove": [
                "zoom",
                "pan",
                "select",
                "lasso",
                "zoomin",
                "autoscale",
                "zoomout",
                "resetscale",
            ],
            "toImageButtonOptions": {
                "filename": download_name,
                "format": st.session_state.image_format,
            },
        },
    )


def download_plotly_figure(fig, filename="", col=""):
    buffer = io.BytesIO()
    fig.write_image(file=buffer, format="png")

    if col:
        col.download_button(
            label=f"Download Figure",
            data=buffer,
            file_name=filename,
            mime="application/png",
        )
    else:
        st.download_button(
            label=f"Download Figure",
            data=buffer,
            file_name=filename,
            mime="application/png",
        )
