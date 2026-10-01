"""Session-state navigation helpers for the Streamlit application."""

import streamlit as st


def initialize_state():
    defaults = {
        "page": "login",
        "user": None,
        "is_admin": False,
        "auth_mode": "login",
        "course_day": 1,
        "quiz_answers": {},
        "quiz_result": None,
    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def navigate(page):
    st.session_state.page = page
    st.rerun()


def logout():
    st.session_state.user = None
    st.session_state.is_admin = False
    st.session_state.page = "login"
    st.session_state.auth_mode = "login"
    st.session_state.quiz_answers = {}
    st.session_state.quiz_result = None
    st.rerun()
