import streamlit as st

# Title for the app
st.title("Your title")

# Header
st.header("Main header")

# Subheader
st.subheader("Subheader")

# Markdown
st.markdown("This is markdown **text**")
st.markdown("# Header 1")
st.markdown("## Header 2")
st.markdown("### Header 3")

# Caption
st.caption("This is a caption")

# Code block
st.code(
"""import pandas as pd
pd.read_csv('my_csv_file.csv')
""")

# Preformatted text
st.text("Some text")

# Latex
st.latex("x = 2^2")

# Divider
st.text("Text above")
st.divider()
st.text("Text below")

# st.write
st.write("Some text")