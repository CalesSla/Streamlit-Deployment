import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

@st.cache_data
def read_data():
    df = pd.read_csv("data/quarterly_canada_population.csv")
    return df

@st.cache_data
def extract_data(df):
    row_names = list(df["Quarter"])
    min_year = min([int(i.split()[1]) for i in row_names])
    max_year = max([int(i.split()[1]) for i in row_names])
    countries_list = sorted(df.columns[2:].tolist())
    countries_list.insert(0, "Canada")
    return row_names, min_year, max_year, countries_list

@st.cache_data
def define_row_indices(row_names, start_row_name, end_row_name):
    try:
        start_row_index = row_names.index(start_row_name)
        end_row_index = row_names.index(end_row_name)
    except ValueError:
        pass
    
    if 'start_row_index' not in locals() or 'end_row_index' not in locals():
        start_row_index, end_row_index = "None", "None"
    return start_row_index, end_row_index



if __name__ == "__main__":
    df = read_data()
    row_names, min_year, max_year, countries_list = extract_data(df)

    url = "https://www.google.com"
    st.title("Population of Canada")
    st.write("Source table can be found [here](%s)" % url)

    with st.expander("See full data table"):
        st.dataframe(df)

    with st.form("Controls form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("##### Choose a starting date")
            start_quarter = st.selectbox("Select start quarter", options=['Q1', 'Q2', 'Q3', 'Q4'], index=2)
            start_year = st.slider("Year", min_value=min_year, max_value=max_year-1, value=min_year)
            start_row_name = str(start_quarter) + " " + str(start_year)

        with col2:
            st.markdown("##### Choose an end date")
            end_quarter = st.selectbox("Select end quarter", options=['Q1', 'Q2', 'Q3', 'Q4'])
            end_year = st.slider("Year", min_value=min_year+1, max_value=max_year, value=max_year)
            end_row_name = str(end_quarter) + " " + str(end_year)

        with col3:
            st.markdown("##### Choose a location")
            country = st.selectbox("Select location", options=countries_list)
        
        start_row_index, end_row_index = define_row_indices(row_names, start_row_name, end_row_name)
        
        analize = st.form_submit_button("Analize", type="primary")

    if (start_row_name not in row_names or end_row_name not in row_names):
        st.error("No data available. Check your quarter and year selection.")
    elif start_row_index >= end_row_index:
        st.error("Dates don't work. Start date must come before end date.")
        
    else:
        tab1, tab2 = st.tabs(["Population change", "Compare"])
        with tab1:   
            st.markdown(f"### Population change in {country} from {start_row_name} to {end_row_name}")
            tab1_col1, tab1_col2 = tab1.columns(2)
            start_year_value = df[df["Quarter"] == f"{start_row_name}"][f"{country}"].values[0]
            end_year_value = df[df["Quarter"] == f"{end_row_name}"][f"{country}"].values[0]
            delta = round((end_year_value - start_year_value) * 100 / start_year_value, 2)
            with tab1_col1:
                st.metric(label=f"{start_row_name}", value=start_year_value)
                st.metric(label=f"{end_row_name}", value=end_year_value, delta=str(delta)+"%")

            with tab1_col2:
                fig1, ax1 = plt.subplots()
                filtered_df = df.loc[start_row_index : end_row_index]
                ax1.plot(filtered_df.Quarter, filtered_df[f'{country}'])
                ax1.set_title(f"Population change in {country} from {start_row_name} to {end_row_name}")
                ax1.set_xlabel("Quarter")
                ax1.set_ylabel("Population")
                ax1.xaxis.set_major_locator(plt.MaxNLocator(8))
                fig1.autofmt_xdate()
                st.pyplot(fig1)


        with tab2:
            st.markdown(f"### Compare with other locations")
            locations = st.multiselect("Choose other locations", countries_list, default=['Yukon', 'Nunavut'])

            fig2, ax2 = plt.subplots()
            ax2.plot(filtered_df.Quarter, filtered_df[locations])
            ax2.set_title(f"Population change from {start_row_name} to {end_row_name}")
            ax2.set_xlabel("Quarter")
            ax2.set_ylabel("Population")
            ax2.xaxis.set_major_locator(plt.MaxNLocator(8))
            
            fig2.autofmt_xdate()
            ax2.legend(locations, loc='center left', bbox_to_anchor=(1, 0.5))
            st.pyplot(fig2)


