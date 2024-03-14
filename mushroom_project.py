import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from itertools import cycle
import pickle
data_path = "data/mushrooms.csv"
features_vocab_file_path = 'data/features_vocab.pickle'

@st.cache_data
def load_feature_vocab(features_vocab_file_path):
    with open(features_vocab_file_path, 'rb') as f:
        features_vocab =  pickle.load(f)
    return features_vocab

@st.cache_data(show_spinner="Fetching data...")
def load_data(path):
    df = pd.read_csv(path)
    return df

@st.cache_data
def update_features_vocab(features_vocab):
    reversed_features_vocab = {}
    for k, v in features_vocab.items():
        features_vocab[k] = dict(sorted(v.items()))
        reversed_features_vocab[k] = {value: key for key, value in v.items()}
    return features_vocab, reversed_features_vocab

@st.cache_resource
def fit_label_encoder(preprocessed_df):
    le = LabelEncoder()
    le.fit(preprocessed_df['class'])
    return le

@st.cache_resource
def fit_ordinal_encoder(preprocessed_df):
    oe = OrdinalEncoder()
    oe.fit(preprocessed_df[preprocessed_df.columns[1:]])
    return oe

@st.cache_data
def select_features(df):
    oe = OrdinalEncoder()
    preprocessed_df = df.copy()
    preprocessed_df[preprocessed_df.columns[1:]] = oe.fit_transform(preprocessed_df[preprocessed_df.columns[1:]])

    X = preprocessed_df.drop(['class'], axis=1)
    y = preprocessed_df['class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, stratify=y, random_state=42)
    
    selector = SelectKBest(mutual_info_classif, k=9)
    selector.fit(X_train, y_train)
    selected_features_mask = selector.get_support()
    selected_features = X_train.columns[selected_features_mask]
    return list(selected_features)


@st.cache_data(show_spinner="Preprocessing data...")
def data_preprocessing(preprocessed_df, _le, _oe):
    
    preprocessed_df['class'] = _le.transform(preprocessed_df['class'])
    preprocessed_df[preprocessed_df.columns[1:]] = _oe.transform(preprocessed_df[preprocessed_df.columns[1:]])

    X = preprocessed_df.drop(['class'], axis=1)
    y = preprocessed_df['class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, stratify=y, random_state=42)

    return preprocessed_df, X_train, X_test, y_train, y_test


@st.cache_resource(show_spinner="Training_model...")
def train_classifier(X_train, y_train, max_depth=5, random_state=42):
    gbc = GradientBoostingClassifier(max_depth=max_depth, random_state=random_state)
    gbc.fit(X_train.values, y_train.values)
    return gbc

@st.cache_data(show_spinner="Making a prediction...")
def make_prediction(_model, _oe, feature_list):
    feature_list_clean = np.array([i[1].split()[0] for i in feature_list]).reshape(1, -1)
    feature_df = pd.DataFrame(feature_list_clean, columns=selected_features)
    feature_list_clean_encoded = _oe.transform(feature_df)
    prediction = _model.predict(feature_list_clean_encoded)[0]
    return prediction
        

if __name__ == "__main__":
    features_vocab = load_feature_vocab(features_vocab_file_path)
    df = load_data(data_path)
    selected_features = select_features(df)
    preprocessed_df = df.copy()[['class'] + selected_features]
    le = fit_label_encoder(preprocessed_df)
    oe = fit_ordinal_encoder(preprocessed_df)

    
    features_vocab, reversed_features_vocab = update_features_vocab(features_vocab)
    preprocessed_df, X_train, X_test, y_train, y_test = data_preprocessing(preprocessed_df, le, oe)
    model = train_classifier(X_train, y_train)
    
    
    st.title("Mushroom classifier :mushroom:")
    with st.expander("See full dataframe"):
        st.dataframe(df)

    st.markdown("### Step 1: Select the values for prediction")
    with st.form("Main form"):
        col1, col2, col3 = st.columns(3)
        feature_list = []
        for col, feature in zip(cycle([col1, col2, col3]), selected_features):
            with col:
                feature_value = st.selectbox(f"**{feature.capitalize()}**", options = [f'{k} - {v}' for k, v in features_vocab[f'{feature}'].items()])
                feature_list.append((feature, feature_value))
        
        prediction = make_prediction(model, oe, feature_list)
        
        predict = st.form_submit_button("Predict", type="primary")
    
    if predict:
        st.write(f"This mushroom is {'poisonous :nauseated_face:' if prediction == 1 else 'edible :fork_and_knife:'}")


    