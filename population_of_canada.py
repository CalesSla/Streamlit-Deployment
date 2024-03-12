import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def convert_to_datetime(data):
    from datetime import datetime

    datetime_list = []

    for quarter in data:
        quarter_number, year = quarter.split()
        if quarter_number == "Q1":
            month = 1
        elif quarter_number == 'Q2':
            month = 4
        elif quarter_number == 'Q3':
            month = 7
        elif quarter_number == 'Q4':
            month = 10
        else:
            raise ValueError("Invalid quarter format")
        
        date_string = f'{month}/01/{year}'
        datetime_list.append(datetime.strptime(date_string, "%m/%d/%Y"))
    return datetime_list




df = pd.read_csv("data/quarterly_canada_population.csv")
df['time'] = convert_to_datetime(df['Quarter'])
row_names = list(df["Quarter"])

url = "https://www.google.com"
st.title("Population of Canada")
st.write("Source table can be found [here](%s)" % url)


with st.expander("See full data table"):
    st.dataframe(df)


with st.form("Controls form"):
    col1, col2, col3 = st.columns(3)

    col1.markdown("##### Choose a starting date")
    col1.write("**Start quarter**")
    start_quarter = col1.selectbox("Select start quarter", options=['Q1', 'Q2', 'Q3', 'Q4'], index=2)
    min_year = min([int(i.split()[1]) for i in row_names])
    max_year = max([int(i.split()[1]) for i in row_names])
    start_year = col1.slider("Year", min_value=min_year, max_value=max_year-1, value=min_year)

    col2.markdown("##### Choose an end date")
    col2.write("**End quarter**")
    end_quarter = col2.selectbox("Select end quarter", options=['Q1', 'Q2', 'Q3', 'Q4'])
    end_year = col2.slider("Year", min_value=min_year+1, max_value=max_year, value=max_year)

    col3.markdown("##### Choose a location")
    col3.write("**Location**")
    countries_list = sorted(df.columns[2:-1].tolist())
    countries_list.insert(0, "Canada")
    country = col3.selectbox("Select location", options=countries_list)

    start_row_name = str(start_quarter) + " " + str(start_year)
    end_row_name = str(end_quarter) + " " + str(end_year)
    
    try:
        start_row_index = row_names.index(start_row_name)
        end_row_index = row_names.index(end_row_name)
    except ValueError:
        pass
    
    analize = st.form_submit_button("Analize")



if (start_row_name not in row_names or end_row_name not in row_names):
    st.error("No data available. Check your quarter and year selection.")
elif start_row_index >= end_row_index:
    st.error("Dates don't work. Start date must come before end date.")
else:
    tab1, tab2 = st.tabs(["Population change", "Compare"])
    tab1.markdown(f"### Population change in {country} from {start_row_name} to {end_row_name}")
    tab1_col1, tab1_col2 = tab1.columns(2)
    start_year_value = df[df["Quarter"] == f"{start_row_name}"][f"{country}"].values[0]
    end_year_value = df[df["Quarter"] == f"{end_row_name}"][f"{country}"].values[0]
    delta = round((end_year_value - start_year_value) * 100 / start_year_value, 2)
    tab1_col1.metric(label=f"{start_row_name}", value=start_year_value)
    tab1_col1.metric(label=f"{end_row_name}", value=end_year_value, delta=str(delta)+"%")


    fig1, ax1 = plt.subplots()
    ax1.plot(df.loc[start_row_index : end_row_index].Quarter, df.loc[start_row_index : end_row_index][f'{country}'])
    ax1.set_title(f"Population change in {country} from {start_row_name} to {end_row_name}")
    ax1.set_xlabel("Quarter")
    ax1.set_ylabel("Population")
    ax1.xaxis.set_major_locator(plt.MaxNLocator(8))
    fig1.autofmt_xdate()
    tab1_col2.pyplot(fig1)


    tab2.markdown(f"### Compare with other locations")
    locations = tab2.multiselect("Choose other locations", countries_list, default=['Yukon', 'Nunavut'])

    fig2, ax2 = plt.subplots()
    ax2.plot(df.loc[start_row_index : end_row_index].Quarter, df.loc[start_row_index : end_row_index][locations])
    ax2.set_title(f"Population change from {start_row_name} to {end_row_name}")
    ax2.set_xlabel("Quarter")
    ax2.set_ylabel("Population")
    ax2.xaxis.set_major_locator(plt.MaxNLocator(8))
    
    fig2.autofmt_xdate()
    ax2.legend(locations, loc='center left', bbox_to_anchor=(1, 0.5))
    tab2.pyplot(fig2)




