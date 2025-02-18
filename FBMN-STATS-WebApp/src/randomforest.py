import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import class_weight
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, accuracy_score

@st.cache_data
def run_random_forest(attribute, n_trees, random_seed=None):
    # initialize a log to print out in the app later
    log = ""

    df_oob = pd.DataFrame()  # Placeholder
    df_important_features = pd.DataFrame()  # Placeholder

    # Placeholder for classification report and label mapping
    class_report = "Classification report here"
    label_mapping = "Label mapping here"

    labels = st.session_state.md[[attribute]]
    rf_data = pd.concat([st.session_state.data, labels], axis=1)

    # Change the values of the attribute of interest from strings to a numerical
    enc = OrdinalEncoder()
    # st.write(labels.value_counts()) # Displays the sample size for each group
    labels = enc.fit_transform(labels)
    labels = np.array([x[0] + 1 for x in labels])

    class_names = enc.categories_[0] #getting the class names

    # Extract the feature intensities as np 2D array
    features = np.array(st.session_state.data)

    # Determine the smallest class size and adjust test_size accordingly
    unique, counts = np.unique(labels, return_counts=True)
    min_class_count = min(counts)
    min_test_size = float(len(unique)) / len(labels)

    # Adjust test size to be larger of the calculated min_test_size or the initial_test_size
    adjusted_test_size = max(min_test_size, 0.25)
    
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size= adjusted_test_size, random_state=random_seed, stratify=labels)

    # Collecting info about feature and label shapes for logging
    log += f"Training Features Shape: {train_features.shape}\n"
    log += f"Training Labels Shape: {train_labels.shape}\n"
    log += f"Testing Features Shape: {test_features.shape}\n"
    log += f"Testing Labels Shape: {test_labels.shape}\n"

    # Balance the weights of the attribute of interest to account for unbalanced sample sizes per group
    sklearn_weights = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_labels),
        y=train_labels)
    
    weights = {}
    for i,w in enumerate(np.unique(train_labels)):
        weights[w] = sklearn_weights[i]

    # Set up the random forest classifier with 100 tress, balanded weights, and a random state to make it reproducible
    rf = RandomForestClassifier(n_estimators=n_trees, class_weight= weights, random_state=random_seed)
   
    # Fit the classifier to the training set
    rf.fit(train_features, train_labels)

    # Use the random forest classifier to predict the sample areas in the test set
    predictions_test = rf.predict(test_features)
    predictions_train = rf.predict(train_features)

    classifier_accuracy = round(rf.score(test_features, test_labels)*100, 2)
    log += f"Classifier mean accuracy score: {classifier_accuracy}%.\n"

    # Calculate confusion matrices
    test_confusion_matrix = confusion_matrix(test_labels, predictions_test, labels=range(len(class_names)))
    train_confusion_matrix = confusion_matrix(train_labels, predictions_train, labels=range(len(class_names)))

    test_confusion_df = pd.DataFrame(test_confusion_matrix, index=class_names, columns=class_names)
    train_confusion_df = pd.DataFrame(train_confusion_matrix, index=class_names, columns=class_names)

    test_accuracy = accuracy_score(test_labels, predictions_test)
    train_accuracy = accuracy_score(train_labels, predictions_train)
    
    # Report of the accuracy of predictions on the test set
    class_report = classification_report(test_labels, predictions_test)

    # Print the sample areas corresponding to the numbers in the report
    label_mapping = "\n".join([f"{i+1.0} ,{cat}" for i, cat in enumerate(enc.categories_[0])])

    # Most important model quality plot
    # OOB error lines should flatline. If it doesn't flatline add more trees
    rf_oob = RandomForestClassifier(class_weight=weights, warm_start=True, oob_score=True, random_state=123)
    errors = []
    tree_range = np.arange(1,500, 10)
    for i in tree_range:
        rf_oob.set_params(n_estimators=i)
        rf_oob.fit(train_features, train_labels)
        errors.append(1-rf_oob.oob_score_)


    df_oob = pd.DataFrame({"n trees": tree_range, "error rate": errors})

    # Extract the important features in the model
    df_important_features = pd.DataFrame(rf.feature_importances_, 
                                         index=st.session_state.data.columns).sort_values(by=0, ascending=False)
    df_important_features.columns = ["importance"]
    
    return df_oob, df_important_features, log, class_report, label_mapping, test_confusion_df, train_confusion_df, test_accuracy, train_accuracy


def get_oob_fig(df):
    return px.line(df, x="n trees", y="error rate", title="out-of-bag (OOB) error")

def classification_report_to_df(report):
    
    # Split the report into lines
    lines = report.split("\n")
    
    # Prepare a dictionary to hold the data
    report_data = {"class": [], "precision": [], "recall": [], "f1-score": [], "support": []}
    
    for line in lines[2:-3]:  # Skip the header and summary lines
        parts = line.split()
        # Ensure that the line contains the expected number of parts
        if len(parts) == 5:
            report_data["class"].append(parts[0])
            report_data["precision"].append(parts[1])
            report_data["recall"].append(parts[2])
            report_data["f1-score"].append(parts[3])
            report_data["support"].append(parts[4])
    
    # Convert the dictionary to a DataFrame
    report_df = pd.DataFrame(report_data)
    
    # Convert numeric columns from strings to floats
    report_df[["precision", "recall", "f1-score"]] = report_df[["precision", "recall", "f1-score"]].astype(float)
    report_df["support"] = report_df["support"].astype(int)
    
    return report_df

def label_mapping_to_df(label_mapping_str):
    
    # Split the string into lines
    lines = label_mapping_str.split("\n")
    
    # Split each line into index and label, then collect into a list of tuples
    mapping = [line.split(" ,") for line in lines if line]  # Ensure the line is not empty
    
    # Convert the list of tuples into a DataFrame
    mapping_df = pd.DataFrame(mapping, columns=['class', 'Label'])
    mapping_df['class'] = mapping_df['class'].astype(str)
    return mapping_df


