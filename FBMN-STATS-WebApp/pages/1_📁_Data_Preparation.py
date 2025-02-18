import streamlit as st
from src.common import *
from src.fileselection import *
from src.cleanup import *
import pandas as pd

page_setup()

st.markdown("# File Selection")

if st.session_state["data_preparation_done"]:
    st.success("Data preparation was successful!")
    if st.button("Re-do the data preparation step now."):
        reset_dataframes()
        st.session_state["data_preparation_done"] = False
        st.rerun()
    show_table(pd.concat([st.session_state.md, st.session_state.data], axis=1), title="FeatureMatrix-scaled-centered")
else:
    st.info(
        """💡 Once you are happy with the results, don't forget to click the **Submit Data for Statistics!** button."""
    )
    ft, md = pd.DataFrame(), pd.DataFrame()

    file_origin = st.radio("File origin", 
                           ["Quantification table and meta data files", 
                            "GNPS(2) task ID", 
                            "Example dataset from publication", 
                            "Small example dataset for testing",
                            "GNPS2 classical molecular networking (CMN)"])
    
    # b661d12ba88745639664988329c1363e
    if file_origin == "Small example dataset for testing":
        ft, md = load_example()

    elif file_origin in ["GNPS(2) task ID", "Example dataset from publication", "GNPS2 classical molecular networking (CMN)"]:
        st.warning("💡 This tool only supports task ID from GNPS1 and 2 not from Quickstart GNPS1.")
        if file_origin == "Example dataset from publication":
            task_id_default = "b661d12ba88745639664988329c1363e" # 63e8b3da08df41fe95031e4710e0476b
            disabled = True
            cmn_flag = False
        elif file_origin == "GNPS2 classical molecular networking (CMN)":
            task_id_default = "" # 2a65f90094654235a4c8d337fdca11e1
            disabled = False
            cmn_flag = True
        else:
            task_id_default = ""
            disabled = False
            cmn_flag = False
        task_id = st.text_input("GNPS task ID", task_id_default, disabled=disabled)
        _, c2, _ = st.columns(3)
        
        if c2.button("Load files from GNPS", type="primary", disabled=len(task_id) == 0, use_container_width=True):
            st.session_state["ft_gnps"], st.session_state["md_gnps"] = load_from_gnps(task_id, cmn= cmn_flag)   
        
        if not st.session_state["ft_gnps"].empty and st.session_state["md_gnps"].empty:
            st.warning("Meta data is empty. Please upload one.")
            
            md_file = st.file_uploader("Meta Data Table")
            if md_file:
                md = load_md(md_file)
                st.success("Meta data was loaded successfully!")
        
        if "ft_gnps" in st.session_state:
            if not st.session_state["ft_gnps"].empty:
                ft = st.session_state["ft_gnps"]

        if "md_gnps" in st.session_state:
            if not st.session_state["md_gnps"].empty:
                md = st.session_state["md_gnps"]

    if file_origin == "Quantification table and meta data files":
        st.info("💡 Upload tables in txt (tab separated), tsv, csv or xlsx (Excel) format.")
        c1, c2 = st.columns(2)
        # Feature Quantification Table
        ft_file = c1.file_uploader("Quantification Table")
        if ft_file:
            st.session_state["ft_uploaded"] = load_ft(ft_file)

        # Meta Data Table
        md_file = c2.file_uploader("Meta Data Table")
        if md_file:
            st.session_state["md_uploaded"] = load_md(md_file)

        if "ft_uploaded" in st.session_state:
            if not st.session_state["ft_uploaded"].empty:
                ft = st.session_state["ft_uploaded"]

        if "md_uploaded" in st.session_state:
            if not st.session_state["md_uploaded"].empty:
                md = st.session_state["md_uploaded"]

    if not ft.empty or not md.empty:
        t1, t2 = st.tabs(["**Quantification Table**", "**Meta Data**"])
        t1.dataframe(ft)
        t2.dataframe(md)

    if not ft.index.is_unique:
        st.error("Please upload a feature matrix with unique metabolite names.")

    if not ft.empty and not md.empty:
        st.success("Files loaded successfully!")

        st.markdown("# Data Cleanup")
        with st.expander("📖 About"):
            st.markdown("**Removal of blank features**")
            st.image("assets/figures/blank-removal.png")
            st.markdown("**Imputation of missing values**")
            st.image("assets/figures/imputation.png")
            st.markdown("**Data scaling and centering**")
            st.image("assets/figures/scaling.png")


        # clean up meta data table
        md = clean_up_md(md)

        # clean up feature table and remove unneccessary columns
        ft = clean_up_ft(ft)

        # # check if ft column names and md row names are the same
        md, ft = check_columns(md, ft)

        # Initialize the process flags at the start of your Streamlit app if they don't already exist
        if 'blank_removal_done' not in st.session_state:
            st.session_state['blank_removal_done'] = False

        if 'imputation_done' not in st.session_state:
            st.session_state['imputation_done'] = False

        # Use a string to track the normalization method used; 'None' indicates no normalization done
        if 'normalization_method_used' not in st.session_state:
            st.session_state['normalization_method_used'] = 'None'

        tabs = st.tabs(["**Blank Removal**", "**Imputation**", "**Normalization**", "📊 **Summary**"])
        with tabs[0]:
            blank_removal = st.checkbox("Remove blank features?", False)
            if blank_removal:
                # Select true sample files (excluding blank and pools)
                st.markdown("#### Samples")
                st.markdown(
                    "Select samples (excluding blank and pools) based on the following table."
                )
                df = inside_levels(md)
                mask = df.apply(lambda row: len(row['LEVELS']) == 0, axis=1)
                df = df[~mask]
                st.dataframe(df)
                c1, c2 = st.columns(2)
                sample_column = c1.selectbox(
                    "attribute for sample selection",
                    md.columns,
                )
                sample_options = list(set(md[sample_column].dropna()))
                sample_rows = c2.multiselect("sample selection", sample_options, sample_options[0])
                samples = ft[md[md[sample_column].isin(sample_rows)].index]
                samples_md = md.loc[samples.columns]

                with st.expander(f"Selected samples preview (n={samples.shape[1]})"):
                    st.dataframe(samples.head())

                if samples.shape[1] == ft.shape[1]:
                    st.warning("You selected everything as sample type. Blank removal not possible.")
                else:
                    v_space(1)
                    # Ask if blank removal should be done
                    st.markdown("#### Blanks")
                    st.markdown(
                        "Select blanks (excluding samples and pools) based on the following table."
                    )
                    non_samples_md = md.loc[
                        [index for index in md.index if index not in samples.columns]
                    ]
                    df = inside_levels(non_samples_md)
                    mask = df.apply(lambda row: len(row['LEVELS']) == 0, axis=1)
                    df = df[~mask]
                    st.dataframe(df)
                    c1, c2 = st.columns(2)

                    blank_column = c1.selectbox(
                        "attribute for blank selection", non_samples_md.columns
                    )
                    blank_options = list(set(non_samples_md[blank_column].dropna()))
                    blank_rows = c2.multiselect("blank selection", blank_options, blank_options[0])
                    blanks = ft[non_samples_md[non_samples_md[blank_column].isin(blank_rows)].index]
                    with st.expander(f"Selected blanks preview (n={blanks.shape[1]})"):
                        st.dataframe(blanks.head())

                    # define a cutoff value for blank removal (ratio blank/avg(samples))
                    c1, c2 = st.columns(2)
                    cutoff = c1.number_input(
                        "cutoff threshold for blank removal",
                        0.1,
                        1.0,
                        0.3,
                        0.05,
                        help="""The recommended cutoff range is between 0.1 and 0.3.
                        Features with intensity ratio of (blank mean)/(sample mean) above the threshold (e.g. 30%) are considered noise/background features.
                        """,
                    )
                    (
                        ft,
                        n_background_features,
                        n_real_features,
                    ) = remove_blank_features(blanks, samples, cutoff)
                    c2.metric("background or noise features", n_background_features)
                    with st.expander(f"Feature table after removing blanks - features: {ft.shape[0]}, samples: {ft.shape[1]}"):
                        show_table(ft, "blank-features-removed")
            
                st.session_state['blank_removal_done'] = True
            else:
                st.session_state['blank_removal_done'] = False
            
            if not ft.empty:
                cutoff_LOD = get_cutoff_LOD(ft)

                with tabs[1]:

                    c1, c2 = st.columns(2)
                    c2.metric(
                        f"total missing values",
                        str((ft == 0).to_numpy().mean() * 100)[:4] + " %",
                    )
                    imputation = c1.checkbox("Impute missing values?", False, help=f"These values will be filled with random number between 1 and {cutoff_LOD} (Limit of Detection) during imputation.")
                    if imputation:
                        if cutoff_LOD > 1:
                            c1, c2 = st.columns(2)
                            ft = impute_missing_values(ft, cutoff_LOD)
                            with st.expander(f"Imputed data - features: {ft.shape[0]}, samples: {ft.shape[1]}"):
                                show_table(ft.head(), "imputed")
                        else:
                            st.warning(f"Can't impute with random values between 1 and lowest value, which is {cutoff_LOD} (rounded).")
                        
                        st.session_state['imputation_done'] = True
                    else:
                        st.session_state['imputation_done'] = False

                with tabs[2]:
                    normalization_method = st.radio("data normalization method", ["None",
                                                            "Center-Scaling", 
                                                            # "Probabilistic Quotient Normalization (PQN)", 
                                                            "Total Ion Current (TIC) or sample-centric normalization"])
                    st.session_state['normalization_method_used'] = normalization_method
                
                with tabs[3]:
                    # Summary tab content
                    st.markdown("## Process Summary")
                    if st.session_state['blank_removal_done']:
                        st.success("Blank removal done.")
                    else:
                        st.warning("Blank removal not done.")

                    if st.session_state['imputation_done']:
                        st.success("Imputation done.")
                    else:
                        st.warning("Imputation not done.")

                    # Check which normalization method was used
                    if st.session_state['normalization_method_used'] != 'None':
                        st.success(f"Normalization done using {st.session_state['normalization_method_used']} method.")
                    else:
                        st.warning("Normalization not done.")

                    tab1, tab2 = st.tabs(
                        ["📊 Feature intensity frequency", "📊 Missing values per feature"]
                    )
                    with tab1:
                        fig = get_feature_frequency_fig(ft)
                        show_fig(fig, "feature-intensity-frequency")
                    with tab2:
                        fig = get_missing_values_per_feature_fig(ft, cutoff_LOD)
                        show_fig(fig, "missing-values")

            
            else:
                st.error("No features left after blank removal!")

        _, c1, _ = st.columns(3)
        if c1.button("**Submit Data for Statistics!**", type="primary"):
            st.session_state["md"], st.session_state["data"] = normalization(
                ft, md, normalization_method
            )
            st.session_state["data_preparation_done"] = True
            st.rerun()