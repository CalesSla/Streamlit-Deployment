import streamlit as st
import pandas as pd
from itertools import cycle
from joblib import load
import numpy as np
data_path = "data/honda_toyota_ca.csv"
model_path = "model.joblib"

@st.cache_data
def load_data(data_path):
    df = pd.read_csv(data_path)
    return df

@st.cache_resource(show_spinner="Loading model...")
def load_model(model_path):
    model = load(model_path)
    return model

def make_prediction(model, category_names):
    prediction = model.predict(np.array([st.session_state[f'{cat}'] for cat in category_names]).reshape(1, -1))
    st.session_state['prediction'] = round(prediction[0])

if __name__ == "__main__":
    df = load_data(data_path)
    model = load_model(model_path)
    category_names = list(df.columns[1:])

    st.title(":maple_leaf: Used car price calculator")

    with st.form("Main form"):
        col1, col2, col3 = st.columns(3)
        
        for col, cat in zip(cycle([col1, col2, col3]), category_names):
            with col:
                if df[f'{cat}'].dtype == "float64" and cat != "year":
                    st.number_input(f'**{cat.capitalize()}**', key=f"{cat}")
                else:
                    st.selectbox(f'**{cat.capitalize()}**', options = sorted([str(i) if cat != 'year' else str(int(i)) for i in df[f"{cat}"].unique()]), key=f"{cat}")

        calculate = st.form_submit_button("Calculate", type="primary", on_click=make_prediction, kwargs=dict(model=model, category_names=category_names))
    
    if 'prediction' in st.session_state.keys():
        st.subheader(f"The estimated car price is {st.session_state['prediction']} $")
    st.write(st.session_state)
