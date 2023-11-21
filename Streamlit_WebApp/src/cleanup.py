import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
# currently conflicting dependencies (requires old pandas 1.2.4)
# from pynmranalysis.normalization import PQN_normalization

@st.cache_data
def clean_up_md(md):
    md = (
        md.copy()
    )  # storing the files under different names to preserve the original files
    # remove the (front & tail) spaces, if any present, from the rownames of md
    md = md.dropna(how="all")
    md.index = [name.strip() for name in md.index]
    # for each col in md
    # 1) removing the spaces (if any)
    # 2) replace the spaces (in the middle) to underscore
    # 3) converting them all to UPPERCASE
    for col in md.columns:
        if md[col].dtype == str:
            md[col] = [item.strip().replace(" ", "_").upper() for item in md[col]]
    md.index = [i.replace(".mzXML", "").replace(".mzML", "").replace(" Peak area", "") for i in md.index]
    return md


@st.cache_data
def clean_up_ft(ft):
    ft = (
        ft.copy()
    )  # storing the files under different names to preserve the original files
    ft = ft.dropna(how="all")
     # drop all columns that are not mzML or mzXML file names
    ft.drop(columns=[col for col in ft.columns if not (".mzML" in col or ".mzXML" in col)], inplace=True)
    # remove " Peak area" from column names, contained after mzmine pre-processing
    ft.rename(
        columns={col: col.replace(" Peak area", "").replace(".mzXML", "").replace(".mzML", "").strip() for col in ft.columns},
        inplace=True,
    )
    return ft


@st.cache_data
def check_columns(md, ft):
    if sorted(ft.columns) != sorted(md.index):
        st.warning("Not all files are present in both meta data & feature table.")
        # print the md rows / ft column which are not in ft columns / md rows and remove them
        ft_cols_not_in_md = [col for col in ft.columns if col not in md.index]
        if ft_cols_not_in_md:
            st.warning(
                f"These {len(ft_cols_not_in_md)} columns of feature table are not present in metadata table and will be removed:\n{', '.join(ft_cols_not_in_md)}"
            )
            ft = ft.drop(columns=ft_cols_not_in_md)
        md_rows_not_in_ft = [row for row in md.index if row not in ft.columns]
        if md_rows_not_in_ft:
            st.warning(
                f"These {len(md_rows_not_in_ft)} rows of metadata table are not present in feature table and will be removed:\n{', '.join(md_rows_not_in_ft)}"
            )
            md = md.drop(md_rows_not_in_ft)
    return md, ft


@st.cache_data
def inside_levels(df):
    df = pd.DataFrame(
        {
            "ATTRIBUTES": df.columns,
            "LEVELS": [set(df[col].dropna().astype(str).to_list()) for col in df],
            "COUNTS": [df[col].value_counts().to_list() for col in df],
        }
    )
    return df


@st.cache_data
def get_cutoff_LOD(df):
    # get the minimal value that is not zero (lowest measured intensity)
    return round(df.replace(0, np.nan).min(numeric_only=True).min())


@st.cache_data
def remove_blank_features(blanks, samples, cutoff):
    # Getting mean for every feature in blank and Samples
    avg_blank = blanks.mean(
        axis=1, skipna=False
    )  # set skipna = False do not exclude NA/null values when computing the result.
    avg_samples = samples.mean(axis=1, skipna=False)

    # Getting the ratio of blank vs samples
    ratio_blank_samples = (avg_blank + 1) / (avg_samples + 1)

    # Create an array with boolean values: True (is a real feature, ratio<cutoff) / False (is a blank, background, noise feature, ratio>cutoff)
    is_real_feature = ratio_blank_samples < cutoff

    # Calculating the number of background features and features present (sum(bg_bin) equals number of features to be removed)
    n_background = len(samples) - sum(is_real_feature)
    n_real_features = sum(is_real_feature)

    blank_removal = samples[is_real_feature.values]

    return blank_removal, n_background, n_real_features


@st.cache_data
def impute_missing_values(df, cutoff_LOD):
    # impute missing values (0) with a random value between one and lowest intensity (cutoff_LOD)
    if cutoff_LOD > 1:
        return df.apply(
            lambda x: [np.random.randint(1, cutoff_LOD) if v == 0 else v for v in x]
        )


@st.cache_resource
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
            "font_color": "#3E3D53",
        },
    )

    return fig


@st.cache_resource
def get_missing_values_per_feature_fig(df, cutoff_LOD):
    # check the number of missing values per feature in a histogram
    n_zeros = df.T.apply(lambda x: sum(x <= cutoff_LOD))

    fig = px.histogram(n_zeros, template="plotly_white", width=600, height=400)

    fig.update_traces(marker_color="#696880")
    fig.update_layout(
        font={"color": "grey", "size": 12, "family": "Sans"},
        title={"text": "MISSING VALUES PER FEATURE", "font_color": "#3E3D53"},
        xaxis_title="number of missing values",
        yaxis_title="count",
        showlegend=False,
        bargap=0.2,
    )
    return fig


@st.cache_data
def normalization(feature_df, meta_data_df, normalization_method):
    feature_df = feature_df.T

    # remove meta data rows that are not samples
    md_rows_not_in_samples = [
        row for row in meta_data_df.index if row not in feature_df.index
    ]
    md_samples = meta_data_df.drop(md_rows_not_in_samples)

    # put the rows in the feature table and metadata in the same order
    feature_df.sort_index(inplace=True)
    md_samples.sort_index(inplace=True)

    try:
        if not list(set(md_samples.index == feature_df.index))[0] == True:
            st.warning("Sample names in feature and metadata table are NOT the same!")
    except:
        st.warning(
            "Sample names in feature and metadata table can NOT be compared. Please check your tables!"
        )

    if normalization_method == "Center-Scaling":
        normalized = pd.DataFrame(
            StandardScaler().fit_transform(feature_df),
            index=feature_df.index,
            columns=feature_df.columns,
        )

    # elif normalization_method == "Probabilistic Quotient Normalization (PQN)":
    #     normalized = PQN_normalization(feature_df ,ref_norm = "median" , verbose=False)

    elif normalization_method == "Total Ion Current (TIC) or sample-centric normalization":
        normalized = feature_df.apply(lambda x: x/np.sum(x), axis=0)
    
    else:
        return md_samples, feature_df
    return md_samples, normalized
