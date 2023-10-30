import streamlit as st
from .common import *

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

@st.cache_data()
def load_from_gnps(task_id, merge_annotations):
    ft_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=quantification_table_reformatted/&block=main"
    md_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=metadata_merged/&block=main"
    an_gnps_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=DB_result/&block=main"
    an_analog_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=DB_analogresult/&block=main"

    ft = pd.read_csv(ft_url)
    ft["metabolite"] = ft.apply(lambda x: str(int(x["row ID"])) + "_" + str(round(x["row m/z"], 4)) + "@" + str(round(x["row retention time"], 2)), axis = 1)
    ft = ft.set_index("metabolite")
    ft = ft[[col for col in ft.columns if not "Unnamed" in col]]
    md = pd.read_csv(md_url, sep = "\t", index_col="filename")

    if merge_annotations:
        an_gnps = pd.read_csv(an_gnps_url, sep = "\t")
        an_analog = pd.read_csv(an_analog_url, sep = "\t")

        # Rename the columns of 'an_analog' with a prefix 'Analog' (excluding the '#Scan#' column)
        an_analog.columns = ['Analog_' + col if col != '#Scan#' else col for col in an_analog.columns]

        # Merge 'an_analog' with 'an_gnps' using a full join on the '#Scan#' column
        an_final = pd.merge(an_gnps, an_analog, on='#Scan#', how='outer')

        # Consolidate multiple annotations for a single '#Scan#' into one combined name
        def combine_names(row):
            if row['Compound_Name'] == row['Analog_Compound_Name']:
                return row['Compound_Name']
            return f"{row['Compound_Name']};{row['Analog_Compound_Name']}"

        an_final_single = an_final.groupby('#Scan#').apply(lambda group: pd.Series({
            'Combined_Name': combine_names(group.iloc[0])
        })).reset_index()

        # To get the DataFrame with that exact column name (without automatic renaming)
        an_final_single.columns = an_final_single.columns.str.replace('.', '_')

        an_final_single = an_final_single.set_index("#Scan#")

        # Annotate metabolites in ft if annotation is available
        ft["metabolite"] = ft.index
        ft["metabolite"] = ft["metabolite"].apply(lambda x: ''.join(i for i in str(x)[:80] if ord(i)<128) if int(x.split("_")[0]) not in an_final_single.index else ''.join(i for i in an_final_single.loc[int(x.split("_")[0]), "Combined_Name"].replace("nan;", "").replace('"', "").replace("'", "")[:80]+f"_{x.split('_')[0]}" if ord(i)<128))

        ft = ft.set_index("metabolite")

   
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
