import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# hashed_pwd = stauth.Hasher(['12345']).generate()
# st.write(hashed_pwd)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login(location='main', fields={'Form name':'Log in', 'Username':'Username', 'Password':'Password', 'Login':'Login'})

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


if authentication_status:
    try:
        if authenticator.reset_password(username, fields={'Form name':'Reset password', 'Current password':'Current password', 'New password':'New password', 'Repeat password': 'Repeat password', 'Reset':'Reset'}):
            with open("config.yaml", "w") as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success("Password modified successfully")
    except Exception as e:
        st.error(e)


try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False, fields={'Form name':'Register user', 'Email':'Email', 'Username':'Username', 'Password':'Password', 'Repeat password':'Repeat password', 'Register':'Register'})
    if email_of_registered_user:
        with open("config.yaml", "w") as file:
            yaml.dump(config, file, default_flow_style=False)
        st.success('User registered successfully')
    
except Exception as e:
    st.error(e)



try:
    username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password()
    if username_of_forgotten_password:
        st.success("New password sent securely")
    elif username_of_forgotten_password == False:
        st.error("Username not found")
except Exception as e:
    st.error(e)


try:
    username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username()
    if username_of_forgotten_username:
        st.success("Username to be sent securely")
    elif username_of_forgotten_username == False:
        st.error("Email not found")
except Exception as e:
    st.error(e)



if st.session_state['authentication_status']:
    try:
        if authenticator.update_user_details(st.session_state['username']):
            with open("config.yaml", "w") as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success("Entries updated successfully")
    except Exception as e:
        st.error(e)


# st.write(st.session_state)