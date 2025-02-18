import streamlit as st
from src.common import *
from src.randomforest import *

page_setup()

st.title("Random Forest")

with st.expander("📖 About"):
    st.markdown(
        """Get the most important features explaining the selected attribute with supervised learning via random forest model."""
    )
    st.image("assets/figures/random-forest.png")

use_random_seed = st.checkbox('Use a fixed random seed for reproducibility', True)

if not st.session_state.data.empty:
    c1, c2 = st.columns(2)
    c1.selectbox(
        "attribute for supervised learning feature classification",
        options=[c for c in st.session_state.md.columns if len(set(st.session_state.md[c])) > 1],
        key="rf_attribute",
    )
    c2.number_input("number of trees", 1, 500, 100, 50,
                    key = "rf_n_trees",
                    help="number of trees for random forest, check the OOB error plot and select a number of trees where the error rate is low and flat")
    
    random_seed = 123 if use_random_seed else None

    if c2.button("Run supervised learning", type="primary"):
        try:
            df_oob, df_important_features, log, class_report, label_mapping, test_confusion_df, train_confusion_df, test_accuracy, train_accuracy = run_random_forest(st.session_state.rf_attribute, st.session_state.rf_n_trees, random_seed)
            st.session_state['df_oob'] = df_oob
            st.session_state['df_important_features'] = df_important_features
            st.session_state['log'] = log
            st.session_state['class_report'] = class_report
            st.session_state['label_mapping'] = label_mapping
            st.session_state['test_confusion_df'] = test_confusion_df
            st.session_state['train_confusion_df'] = train_confusion_df
            st.session_state['test_accuracy'] = test_accuracy
            st.session_state['train_accuracy'] = train_accuracy
        except Exception as e:
            st.error(f"Failed to run model due to: {str(e)}")

if 'df_important_features' in st.session_state and not st.session_state.df_important_features.empty:
    tabs = st.tabs(["📈 Analyze optimum number of trees", 
                    "📁 Feature ranked by importance", 
                    "📋 Classification Report",
                    "🔍 Confusion Matrix"])
    with tabs[0]:
        fig = get_oob_fig(st.session_state.df_oob)
        show_fig(fig, "oob-error")
    with tabs[1]:
        show_table(st.session_state.df_important_features)
    with tabs[2]:  # Classification Report
        if 'log' in st.session_state:
            st.subheader("Log Messages")
            st.text(st.session_state.log)

        if 'class_report' in st.session_state and 'label_mapping' in st.session_state:
            st.subheader("Classification Report")
        
            # Convert the classification report string to DataFrame
            class_report_df = classification_report_to_df(st.session_state.class_report)
        
            # Convert the label mapping string to DataFrame
            label_mapping_df = label_mapping_to_df(st.session_state.label_mapping)
           
            # Ensure class_report_df's index is set correctly for merging
            class_report_df['class'] = class_report_df['class'].astype(str)
        
            # Merge the DataFrames on 'Class Index'
            merged_df = pd.merge(class_report_df, label_mapping_df, on='class')
            merged_df.set_index('Label', inplace=True)
            st.dataframe(merged_df)
    with tabs[3]:
        st.subheader("Test Set Confusion Matrix")
        st.dataframe(st.session_state.test_confusion_df)
        st.write(f"Test Set Accuracy: {st.session_state.test_accuracy:.2%}")

        st.subheader("Train Set Confusion Matrix")
        st.dataframe(st.session_state.train_confusion_df)
        st.write(f"Train Set Accuracy: {st.session_state.train_accuracy:.2%}")