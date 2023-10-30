import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import class_weight
from sklearn.metrics import classification_report

@st.cache_data
def run_random_forest(attribute, n_trees):
    # initialize a log to print out in the app later
    log = ""

    labels = st.session_state.md[[attribute]]
    rf_data = pd.concat([st.session_state.data, labels], axis=1)

    # Change the values of the attribute of interest from strings to a numerical
    enc = OrdinalEncoder()
    # st.write(labels.value_counts()) # Displays the sample size for each group
    labels = enc.fit_transform(labels)
    labels = np.array([x[0] + 1 for x in labels])

    # Extract the feature intensities as np 2D array
    features = np.array(st.session_state.data)


    # Split the data into training and test sets
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25, random_state=123)

    print(f'Training Features Shape: {train_features.shape}')
    print(f'Training Labels Shape: {train_labels.shape}')
    print(f'Testing Features Shape: {test_features.shape}')
    print(f'Testing Labels Shape: {test_labels.shape}')

    # Balance the weights of the attribute of interest to account for unbalanced sample sizes per group
    sklearn_weights = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_labels),
        y=train_labels)
    weights = {}
    for i,w in enumerate(np.unique(train_labels)):
        weights[w] = sklearn_weights[i]

    # Set up the random forest classifier with 100 tress, balanded weights, and a random state to make it reproducible
    rf = RandomForestClassifier(n_estimators=n_trees, class_weight=weights, random_state=123)
    # Fit the classifier to the training set
    rf.fit(train_features, train_labels)

    # Use the random forest classifier to predict the sample areas in the test set
    predictions = rf.predict(test_features)
    print(f'Classifier mean accuracy score: {round(rf.score(test_features, test_labels)*100, 2)}%.')

    # Report of the accuracy of predictions on the test set
    print(classification_report(test_labels, predictions))

    # Print the sample areas corresponding to the numbers in the report
    print("Sample areas corresponding to the numbers:")
    for i,cat in enumerate(enc.categories_[0]):
        print(f"{i+1.0} ,{cat}")

    # Most important model quality plot
    # OOB error lines should flatline. If it doesn't flatline add more trees
    rf = RandomForestClassifier(class_weight=weights, warm_start=True, oob_score=True, random_state=123)
    errors = []
    tree_range = np.arange(1,500, 10)
    for i in tree_range:
        rf.set_params(n_estimators=i)
        rf.fit(train_features, train_labels)
        errors.append(1-rf.oob_score_)


    df_oob = pd.DataFrame({"n trees": tree_range, "error rate": errors})

    # Extract the important features in the model
    df_important_features = pd.DataFrame(rf.feature_importances_, index=st.session_state.data.columns).sort_values(by=0, ascending=False)
    df_important_features.columns = ["importance"]


    return df_oob, df_important_features

def get_oob_fig(df):
    return px.line(df, x="n trees", y="error rate", title="out-of-bag (OOB) error")