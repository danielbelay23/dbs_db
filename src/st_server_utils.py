import streamlit as st
from .logging import logger
from urllib.parse import unquote

from config import NAV_STRUCTURE
import os

asset_dir = os.path.join(os.path.dirname(__file__), "..", "assets")

def get_headers():
    headers = st.context.headers
    return headers

def get_loggedin_username_and_email():
    """return logged in user email adress or None if no headers were found"""
    headers = get_headers()  # your way to access request headers

    cookie = headers.get("Cookie", "")
    if cookie:
        logger.info(cookie)
        cookie_dct = {
            k.strip(): unquote(v)
            for k, v in map(lambda x: x.split("=", 1), cookie.split(";"))
        }
        user_name = cookie_dct.get("OauthName", "")
        user_email = cookie_dct.get("OauthEmail", "")
        user_groups = cookie_dct.get("OauthGroups", "")
    else:
        logger.warning("cannot get user_name from cookie")
        user_name = ""
        user_email = ""
        user_groups = ""
    return user_name, user_email, user_groups

def create_navigation():
    """Creates the navigation sidebar with the home page and projects under an st.expander"""
    
    css_file = os.path.join(asset_dir, "styling.css")
    with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
    
    st.sidebar.page_link("about_daniel_belay.py", label="about daniel belay")
    with st.sidebar.expander("one-off projects", expanded=True):
        for section_name, section_config in NAV_STRUCTURE.items():
            for page in section_config["pages"]:
                st.page_link(page["path"], label=page["title"])
