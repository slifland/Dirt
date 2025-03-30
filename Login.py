import streamlit as st
import requests
from requests_oauthlib import OAuth2Session
import os
import extra_streamlit_components as stx
import database_manager
import asyncio
import webbrowser

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

def get_manager():
    return stx.CookieManager()


manager = None
cookies = st.context.cookies
if not "user_logged_in" in cookies:
    manager = get_manager()
    if manager.get("user_logged_in") is None:
        manager.set("user_logged_in", False)
        st.rerun()
elif "user_logged_in" in cookies:
    value = cookies["user_logged_in"]
    if value == 'true':
        st.session_state.authenticated = True


# Google OAuth configuration
client_id = "8378098624-ugfuo7avsq8b24lf28pkctk55c695e8j.apps.googleusercontent.com"
client_secret = "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"
authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
token_url = "https://oauth2.googleapis.com/token"
redirect_uri = "https://slifland-dirt-login-dtdc06.streamlit.app"
scope = ["https://www.googleapis.com/auth/userinfo.email", 
         "https://www.googleapis.com/auth/userinfo.profile", 
         "openid"]

# Initialize the OAuth session
if 'oauth_state' not in st.session_state:
    st.session_state.oauth_state = None

def get_oauth_session():
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope, state=st.session_state.oauth_state)

# Check authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Check for callback from OAuth provider
    query_params = st.query_params
    
    if 'code' in query_params:
        st.write("Received code, attempting to exchange for token...")
        oauth = get_oauth_session()
        try:
            token = oauth.fetch_token(
                token_url,
                client_secret=client_secret,
                code=query_params['code'],
                include_client_id=True
            )
            
            # Get user info from the provider
            user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
            user_info = oauth.get(user_info_url).json()
            # Store in session state
            st.session_state.user_info = user_info
            st.session_state.authenticated = True
            new_user = {"id": user_info['id'], "score": 0}
            database_manager.add_user_if_necessary(new_user)
            if not manager:
                cookie_manager = get_manager()
            else:
                cookie_manager = manager
            cookie_manager.set("user_id", user_info['id'], key='userid', max_age=2592000)
            
            # Clear query parameters to avoid token reuse
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            st.write("Error details:", e)
    else:
        # Initial load - show login button
        st.title("Please Log In")
        
        if st.button("Login with Google"):
            oauth = get_oauth_session()
            authorization_url, state = oauth.authorization_url(
                authorization_base_url,
                access_type="offline",  # Get refresh token too
                prompt="select_account"  # Force account selection
            )
            st.session_state.oauth_state = state
            
            st.write(f"Redirecting to: {authorization_url}")
            
            webbrowser.open(authorization_url)
    
else:
    if not manager:
        cookie_manager = get_manager()
    else:
        cookie_manager = manager
    cookie_manager.set("user_logged_in", True, key='user_logged_in', max_age=2592000)
    st.write("You are logged in!")
    st.session_state.logged_in = True
    st.switch_page("pages/app.py")
