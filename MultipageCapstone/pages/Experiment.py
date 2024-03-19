import streamlit as st
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
init_state_vars = ("score", "model", "num_features")

st.set_page_config(page_title="Experiment",
                   page_icon="✅",
                   layout="wide",
                   initial_sidebar_state="auto")

def init_state(init_state_vars):
    if all(key not in st.session_state.keys() for key in init_state_vars):
        for var in init_state_vars:
            st.session_state[var] = {}

@st.cache_data
def load_data():
    data = load_wine(as_frame=True)
    df = pd.DataFrame(data.data, columns = data.feature_names)
    df['target'] = data.target
    return df

@st.cache_data
def define_train_test(df):
    X = df.drop("target", axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    return X, y, X_train, X_test, y_train, y_test

@st.cache_data
def select_best(X_train, y_train, k):
    selector = SelectKBest(mutual_info_classif, k=k)
    selector.fit(X_train, y_train)

    sel_X_train = selector.transform(X_train)
    sel_X_test = selector.transform(X_test)
    return sel_X_train, sel_X_test

@st.cache_data
def make_prediction(cls_name, sel_X_train, y_train, sel_X_test):
    if cls_name == "Baseline":
        cls = DummyClassifier(strategy='most_frequent', random_state=42)
    elif cls_name == "Decision Tree":
        cls = DecisionTreeClassifier(random_state=42)
    elif cls_name == "Random Forest":
        cls = RandomForestClassifier(random_state=42)
    elif cls_name == "Gradient Boosted Classifier":
        cls = GradientBoostingClassifier(random_state=42)
    else:
        raise ValueError("Sorry, wrong classifier name")
    cls.fit(sel_X_train, y_train)
    pred = cls.predict(sel_X_test)

    return pred


def run_pipeline(X_train, y_train, k, model_name):
    sel_X_train, sel_X_test = select_best(X_train, y_train, k=k)
    pred = make_prediction(model_name, sel_X_train, y_train, sel_X_test)
    f1 = f1_score(y_test, pred, average="weighted")
    st.session_state['model'][len(st.session_state['score'])] = model_name
    st.session_state['num_features'][len(st.session_state['score'])] = k
    st.session_state['score'][len(st.session_state['score'])] = f1

init_state(init_state_vars)
df = load_data()
X, y, X_train, X_test, y_train, y_test = define_train_test(df)

st.title(":white_check_mark: Experiments")

col1, col2 = st.columns(2)

with col1:
    model_name = st.selectbox("Choose a model", options=["Baseline", "Decision Tree", "Random Forest", "Gradient Boosted Classifier"])
with col2:
    k = st.number_input("Choose the number of features to keep", min_value=1, max_value=len(df.columns)-1)

st.button("Train", type="primary", on_click=run_pipeline, kwargs=dict(X_train=X_train, y_train=y_train, k=k, model_name=model_name))

with st.expander("See full dataset"):
    st.write(df)

if len(st.session_state['score']) > 0:
    st.subheader(f"The model has an F1-Score of: {st.session_state['score'][len(st.session_state['score'])-1]}")

# st.write(st.session_state)