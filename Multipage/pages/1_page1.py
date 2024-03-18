import streamlit as st

st.title("First page")

x1 = st.session_state['x1']
x2 = st.session_state['x2']

st.subheader(f"You chose to multiply {x1} with {x2}")
st.markdown("""### Check the next page for the result!""")

st.write(st.session_state['df'])

st.write(st.session_state)