import streamlit as st
import pandas as pd

primary_btn = st.button(label = "Primary", type = 'primary')
secondary_btn = st.button(label="Secondary", type = "secondary")

if primary_btn:
    st.write("Hello from primary")

if secondary_btn:
    st.write("Hello from secondary")

st.divider()

checkbox = st.checkbox("Remember be")
if checkbox:
    st.write("I will remember you")
else:
    st.write("I will forget you")

st.divider()

df = pd.read_csv("data/sample.csv")

radio = st.radio("Choose a column", options = df.columns[1:], index = 1, horizontal = True)
st.write(radio)

st.divider()

select = st.selectbox("Choose a column", options=df.columns[1:], index=0)
st.write(select)

st.divider()

multiselect = st.multiselect("Choose as many columns as you want", options=df.columns[1:], default=["col2"], max_selections=2)
st.write(multiselect)

st.divider()

slider = st.slider("Pick a number", min_value=0, max_value=10, value=0, step=1)
st.write(slider)

st.divider()

text_input = st.text_input("What's your name?", placeholder="John Doe")
st.write(f"Your name is {text_input}")

st.divider()

num_input = st.number_input("Pick a number", min_value=0, max_value=10, value=0, step=1)
st.write(f"You picked {num_input}")

st.divider()

txt_area = st.text_area("What do you want to tell me?", height=200, placeholder="Write your message here")
