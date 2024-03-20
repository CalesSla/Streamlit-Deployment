import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
import numpy as np

# hashed_pwd = stauth.Hasher(['12345']).generate()
# st.write(hashed_pwd)

@st.cache_data
def load_data(data_path):
    df = pd.read_csv(data_path)
    return df

@st.cache_data
def train_clusters(modelling_df):
    sil_scores_kmeans = []
    sil_scores_agglo = []
    kmeans_algorithms = []
    for i in range(2, 11):
        kmeans = KMeans(n_clusters=i, random_state=42).fit(modelling_df)
        preds_kmeans = kmeans.predict(modelling_df)
        preds_agglo = AgglomerativeClustering(n_clusters=i).fit_predict(modelling_df)
        sil_score_kmeans = silhouette_score(modelling_df, preds_kmeans)
        sil_score_agglo = silhouette_score(modelling_df, preds_agglo)
        sil_scores_kmeans.append(sil_score_kmeans)
        sil_scores_agglo.append(sil_score_agglo)
        kmeans_algorithms.append(kmeans)
    return sil_scores_kmeans, sil_scores_agglo, kmeans_algorithms

@st.cache_data
def run_experiments_func(modelling_df):
    sil_scores_kmeans, sil_scores_agglo, kmeans_algorithms = train_clusters(modelling_df)
    st.session_state['results_df'] = pd.DataFrame({"n_clusters": np.arange(2, 11), "KMeans": sil_scores_kmeans, "Agglo": sil_scores_agglo})
    st.session_state['kmeans_algorithms'] = kmeans_algorithms

# @st.cache_data
def use_groups(groups, slider_value, df):
    st.session_state['group_numbers'] = []
    st.session_state['sex_values'] = []
    st.session_state['marital_status'] = []
    st.session_state['ages'] = []
    st.session_state['education'] = []
    st.session_state['city_size'] = []
    st.session_state['income'] = []
    st.session_state['display_groups'] = True
    city_size_dict = {0: "Small-sized city", 1: "Mid-sized city", 2: "Large city"}
    for i in range(slider_value):
        group_df = df[groups == i]
        st.session_state['group_numbers'].append(i+1)
        sex_values = group_df['Sex'].value_counts()
        st.session_state['sex_values'].append((round(sex_values[0]*100/sum(sex_values)), round(sex_values[1]*100/sum(sex_values))))
        marital_status = group_df["Marital status"].value_counts()
        st.session_state['marital_status'].append(round(marital_status[0]*100/sum(marital_status)))
        mean_age = round(np.mean(group_df['Age']))
        max_age = max(group_df['Age'])
        min_age = min(group_df["Age"])
        st.session_state['ages'].append((mean_age, max_age, min_age))
        income = group_df["Education"].value_counts()
        high_school = (income[1]) * 100 / sum(income)
        university = (income[0]) * 100 / sum(income)
        st.session_state['education'].append((round(high_school), round(university)))
        income = group_df['Income']
        mean_income = round(np.mean(group_df['Income']))
        max_income = max(group_df['Income'])
        min_income = min(group_df["Income"])
        st.session_state['income'].append((mean_income, max_income, min_income))
        city_size = group_df['Settlement size'].value_counts().idxmax()
        st.session_state['city_size'].append(city_size_dict[city_size])
    
@st.cache_data
def display_gruops(number_of_groups):
    for i in range(number_of_groups):
        st.header(f"Group {i+1}")
        st.subheader("Demographics")
        st.write(f"Percentage of men: {st.session_state['sex_values'][i][0]}%")
        st.write(f"Percentage of women: {st.session_state['sex_values'][i][1]}%")
        st.subheader(f"Marital status")
        st.write(f"Percentage of married clients: {st.session_state['marital_status'][i]}%")
        st.subheader(f"Age")
        st.write(f"Mean age: {st.session_state['ages'][i][0]}")
        st.write(f"Max age: {st.session_state['ages'][i][1]}")
        st.write(f"Min age: {st.session_state['ages'][i][2]}")
        st.subheader(f"Education")
        st.write(f'High school: {st.session_state["education"][i][0]}%')
        st.write(f'University: {st.session_state["education"][i][1]}%')
        st.subheader("Income")
        st.write(f"Mean income: {st.session_state['income'][i][0]}$")
        st.write(f"Max income: {st.session_state['income'][i][1]}$")
        st.write(f"Min income: {st.session_state['income'][i][2]}$")
        st.subheader("City size")
        st.write(f"The majority is: {st.session_state['city_size'][i]}")

@st.cache_data
def generate_groups_func(slider_value, modelling_df):
    if "kmeans_algorithms" in st.session_state.keys():
        kmeans = st.session_state['kmeans_algorithms'][slider_value-2]
        groups = kmeans.predict(modelling_df)
    else:
        st.error("Generate your groups to display them first")
    use_groups(groups, slider_value, modelling_df)

if 'display_groups' not in st.session_state.keys():
    st.session_state['display_groups'] = False

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login(location='sidebar')

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

if st.session_state['authentication_status'] is None:
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False, fields={'Form name':'Register user', 'Email':'Email', 'Username':'Username', 'Password':'Password', 'Repeat password':'Repeat password', 'Register':'Register'}, location='sidebar')
        if email_of_registered_user:
            with open("config.yaml", "w") as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success('User registered successfully')
        
    except Exception as e:
        st.error(e)

if st.session_state['authentication_status']:
    df = load_data("data/segmentation data.csv")
    modelling_df = df[df.columns[1:]]

    if st.session_state['username'] == "datascience":
        st.write(df)
        
        results_df = st.button("Run experiments", on_click=run_experiments_func, args=(modelling_df,))
        if 'results_df' in st.session_state.keys():
            st.markdown("##### Silhouette scores")
            st.write(st.session_state['results_df'])
    elif st.session_state['username'] == "marketing":
        df = load_data("data/segmentation data.csv")
        st.write(df)

        slider_value = st.slider("Number of groups", min_value=2, max_value=10, step=1)
        button_clicked = st.button("Generate groups")
    

        if button_clicked:
            generate_groups_func(slider_value=slider_value, modelling_df=modelling_df)
        if 'group_numbers' in st.session_state.keys():
            display_gruops(len(st.session_state['group_numbers']))
    
