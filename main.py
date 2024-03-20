import pandas as pd
from supabase import create_client, Client
import streamlit as st

@st.cache_resource
def init_connection():
    url: str = st.secrets['supabase_url']
    key: str = st.secrets['supabase_key']
    client: Client = create_client(url, key)
    return client

supabase = init_connection()

@st.cache_data(ttl=600)
def run_query():
    # return supabase.table("car_parts_monthly_sales").select('*').execute()
    return supabase.table("car_parts_monthly_sales").select("*").eq("parts_id", 2674).execute()

st.title("Query a database")

rows = run_query()
df = pd.json_normalize(rows.data)
st.write(df)