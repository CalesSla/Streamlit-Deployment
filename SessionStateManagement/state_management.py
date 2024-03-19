import streamlit as st

st.title("Stateful apps")

st.write("Here is the session state:")
st.write(st.session_state)
st.button("Update state")

if "key" not in st.session_state:
    st.session_state['key'] = "value"

if "attribute" not in st.session_state:
    st.session_state.attribute = "another value"


st.write(f"Reading with key-value syntax: {st.session_state['key']}")
st.write(f"Reading with the attribute syntax: {st.session_state.attribute}")

st.session_state['key'] = "new value"
st.session_state.attribute = "updated value"


del st.session_state['key']