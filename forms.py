import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

with st.form("What would you like to order"):
    st.write("**What would you like to order?**")
    apperitizer = st.selectbox("**Appetizers**", options=['appetizer1', 'appetizer2'])
    main_course = st.selectbox("**Main course**", options=['main1', 'main2'])
    dessert = st.selectbox("**Dessert**", options=['dessert1', 'dessert2'])
    bringing_wine = st.checkbox("**Are you bringing your own wine?**")
    coming_date = st.date_input("**When are you coming?**", min_value=datetime.now(), max_value=datetime.now() + timedelta(days=7))
    time_coming = st.time_input("**What time?**")
    allergies = st.text_area("**Any allergies?**")

    submitted = st.form_submit_button("Submit")

st.write(f"""
Appetizer: {apperitizer}

Main course: {main_course}

{"I am bringing my wine" if bringing_wine else "I am not bringing wine"}

Date coming: {str(coming_date)}

Time coming: {str(time_coming)}

Allergies: {allergies}
""")