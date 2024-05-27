import streamlit as st
from .common import *
from gnpsdata import taskresult
from gnpsdata import workflow_fbmn
import urllib

patterns = [
    ["m/z", "mz", "mass over charge"],
    ["rt", "retention time", "retention-time", "retention_time"],
]


def string_overlap(string, options):
    for option in options:
        if option in string and "mzml" not in string:
            return True
    return False


def get_new_index(df):
    # get m/z values (cols[0]) and rt values (cols[1]) column names
    cols = [
        [col for col in df.columns.tolist() if string_overlap(col.lower(), pattern)]
        for pattern in patterns
    ]
    try:
        # select the first match for each
        column_names = [col[0] for col in cols if col]
        if not column_names:
            return df, "no matching columns"
        # set metabolites column with index as default
        df["metabolite"] = df.index
        if len(column_names) == 2:
            df["metabolite"] = df[column_names[0]].round(5).astype(str)
            if column_names[1]:
                df["metabolite"] = (
                    df["metabolite"] + "@" + df[column_names[1]].round(2).astype(str)
                )
            if "row ID" in df.columns:
                df["metabolite"] = df["row ID"].astype(str) + "_" + df["metabolite"]
        df.set_index("metabolite", inplace=True)
    except:
        return df, "fail"
    return df, "success"


allowed_formats = "Allowed formats: csv (comma separated), tsv (tab separated), txt (tab separated), xlsx (Excel file)."


def load_example():
    ft = open_df("example-data/FeatureMatrix.csv")
    ft, _ = get_new_index(ft)
    md = open_df("example-data/MetaData.txt").set_index("filename")
    return ft, md

@st.cache_data
def load_from_gnps(task_id, cmn=False):

    try: # GNPS2 will run here
        ft = workflow_fbmn.get_quantification_dataframe(task_id, gnps2=True)
        md = workflow_fbmn.get_metadata_dataframe(task_id, gnps2=True).set_index("filename")
        an = taskresult.get_gnps2_task_resultfile_dataframe(task_id, "nf_output/library/merged_results_with_gnps.tsv")[["#Scan#", "Compound_Name"]].set_index("#Scan#")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error encountered: {e}") # GNPS1 task IDs can not be retrieved and throw HTTP Error 500
        if cmn:
            ft_url = f"https://gnps2.org/resultfile?task={task_id}&file=nf_output/clustering/featuretable_reformatted_precursorintensity.csv"
            md_url = f"https://gnps2.org/resultfile?task={task_id}&file=nf_output/metadata/merged_metadata.tsv"
            
            ft = pd.read_csv(ft_url)
            try:
                md = pd.read_csv(md_url, sep = "\t", index_col="filename")
            except pd.errors.EmptyDataError:
                md = pd.DataFrame()

        else:
            ft_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=quantification_table_reformatted/&block=main"
            md_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=metadata_merged/&block=main"
            an_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=DB_result/&block=main"

            ft = pd.read_csv(ft_url)
            md = pd.read_csv(md_url, sep="\t", index_col="filename")
            an = pd.read_csv(an_url, sep = "\t")[["#Scan#", "Compound_Name"]].set_index("#Scan#")

    if md.empty: # Handle empty metadata
        md = pd.DataFrame()

    if cmn:
        ft.index = ft["row ID"].astype(str)
        ft = ft.drop(columns=["row m/z", "row retention time", "row ID"])

    else:
        index_with_mz_RT = ft.apply(lambda x: f'{x["row ID"]}_{round(x["row m/z"], 4)}_{round(x["row retention time"], 2)}', axis=1)
        ft.index = index_with_mz_RT
        if 'df_gnps_annotations' in st.session_state:
            st.session_state["df_gnps_annotations"].index = index_with_mz_RT
            st.session_state["df_gnps_annotations"]["GNPS annotation"] = ft["row ID"].apply(lambda x: an.loc[x, "Compound_Name"] if x in an.index else pd.NA)
            st.session_state["df_gnps_annotations"].dropna(inplace=True)
    
    ft.index.name = 'metabolite'
    return ft, md


def load_ft(ft_file):
    ft = open_df(ft_file)
    ft = ft.dropna(axis=1)
    # determining index with m/z, rt and adduct information
    if "metabolite" in ft.columns:
        ft.index = ft["metabolite"]
    else:
        v_space(2)
        st.warning(
            """⚠️ **Feature Table**

No **'metabolite'** column for unique metabolite ID specified.

Please select the correct one or try to automatically create an index based on RT and m/z values."""
        )
        if st.checkbox("Create index automatically", value=True):
            ft, msg = get_new_index(ft)
            if msg == "no matching columns":
                st.warning(
                    "Could not determine index automatically, missing m/z and/or RT information in column names."
                )
        else:
            metabolite_col = st.selectbox(
                "Column with unique values to use as metabolite ID.",
                [col for col in ft.columns if not col.endswith("mzML") if len(ft[col]) == len(set(ft[col]))],
            )
            if metabolite_col:
                ft = ft.rename(columns={metabolite_col: "metabolite"})
                ft.index = ft["metabolite"].astype(str)
                ft = ft.drop(columns=["metabolite"])
    if ft.empty:
        st.error(f"Check quantification table!\n{allowed_formats}")
    return ft


def load_md(md_file):
    md = open_df(md_file)
    # we need file names as index, if they don't exist throw a warning and let user chose column
    if "filename" in md.columns:
        md.set_index("filename", inplace=True)
    else:
        v_space(2)
        st.warning(
            """⚠️ **Meta Data Table**

No 'filename' column for samples specified.

Please select the correct one."""
        )
        filename_col = st.selectbox("Column to use for sample file names.", [col for col in md.columns if len(md[col]) == len(set(md[col]))])
        if filename_col:
            md = md.set_index(filename_col)
            md.index = md.index.astype(str)
    if md.empty:
        st.error(f"Check meta data table!\n{allowed_formats}")

    return md
