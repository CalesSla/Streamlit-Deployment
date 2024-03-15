import streamlit as st

def add_temp_delta(num):
    st.session_state['celsius'] = st.session_state['celsius'] + num
    change_celsius()

def change_celsius():
    st.session_state['fahrenheit'] = st.session_state['celsius']*1.8 + 32
    st.session_state['kelvin'] = st.session_state['celsius'] + 273.15

def change_fahrenheit():
    st.session_state['celsius'] = (st.session_state['fahrenheit']-32) * (5/9)
    st.session_state['kelvin'] = (st.session_state['fahrenheit']-32) * (5/9) + 273.15

def change_kelvin():
    st.session_state['celsius'] = st.session_state['kelvin'] - 273.15
    st.session_state['fahrenheit'] = (st.session_state['kelvin'] - 273.15) * (9/5) + 32

def set_temperatures(celsius):
    st.session_state['celsius'] = celsius
    change_celsius()

st.title("State management with temperatures")
st.subheader("Temperature conversion")

col1, col2, col3 = st.columns(3)



if "celsius" not in st.session_state:
    st.session_state['celsius'] = 0
col1.number_input("Celsius", key='celsius', on_change=change_celsius)

if "add_celsius" not in st.session_state:
    st.session_state['add_celsius'] = 10
num = col1.number_input("Add to Celsius", step=1, key='add_celsius')


if "fahrenheit" not in st.session_state:
    st.session_state['fahrenheit'] = st.session_state['celsius']*1.8 + 32
col2.number_input("Fahrenheit", key='fahrenheit', on_change=change_fahrenheit)

if "kelvin" not in st.session_state:
    st.session_state['kelvin'] = st.session_state['celsius'] + 273.15
col3.number_input("Kelvin", key='kelvin', on_change=change_kelvin)




st.button("Add", type="primary", on_click=add_temp_delta, args=(num, ))




col4, col5, col6 = st.columns(3)

col4.button(":ice_cube: Freezing point of water", on_click=set_temperatures, kwargs=dict(celsius=0.00))

col5.button(":fire: Boiling point of water", on_click=set_temperatures, kwargs=dict(celsius=100.00))

col6.button(":cold_face: Absolute zero", on_click=set_temperatures, kwargs=dict(celsius=-273.15))

st.write(st.session_state)