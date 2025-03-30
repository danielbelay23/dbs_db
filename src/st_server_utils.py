from .logging import logger
from urllib.parse import unquote
from streamlit.web.server.websocket_headers import (
    get_script_run_ctx,
)
import streamlit as st


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
