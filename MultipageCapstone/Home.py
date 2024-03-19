import streamlit as st
import pandas as pd
from pages.Experiment import init_state
init_state_vars = ("score", "model", "num_features")

st.set_page_config(page_title="Home",
                   page_icon=":house:",
                   layout="wide",
                   initial_sidebar_state="auto")

init_state(init_state_vars)

st.title(":trophy: Model ranking")

try:
    a = st.session_state['score'][0]
    data = {"Model" : st.session_state['model'], "Number of features": st.session_state['num_features'], "F1-Score" : st.session_state['score']}
    df = pd.DataFrame(data).sort_values(by=["F1-Score", "Number of features"], ascending=[False, True]).reset_index(drop=True)
    st.write(df)
except KeyError:
    st.subheader("Train a model in the next page to see the results :point_right:")


st.write(st.session_state)