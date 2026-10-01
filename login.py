"""Learner sign-in and registration forms."""

import re

import streamlit as st

import database


def _valid_details(name, email):
    if not name:
        return "Enter your name."
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return "Enter a valid email address."
    return None


def _start_session(learner):
    st.session_state.user = {
        "id": learner[0],
        "name": learner[1],
        "email": learner[2],
    }
    st.session_state.is_admin = False
    st.session_state.page = "dashboard"
    st.session_state.quiz_result = None
    st.rerun()


def render_login():
    st.title("Internet Basics")
    st.subheader("Learner access")
    sign_in, register = st.tabs(["Sign in", "Create account"])

    with sign_in:
        with st.form("learner_login_form"):
            name = st.text_input("Student name")
            email = st.text_input("Email address")
            submitted = st.form_submit_button("Start learning", type="primary")

        if submitted:
            name = name.strip()
            email = email.strip().lower()
            validation_error = _valid_details(name, email)
            if validation_error:
                st.warning(validation_error)
            else:
                learner = database.get_learner(name, email)
                if learner:
                    _start_session(learner)
                else:
                    st.error("No account matches those details. Create an account first.")

    with register:
        with st.form("learner_registration_form"):
            name = st.text_input("Full name", key="register_name")
            email = st.text_input("Email address", key="register_email")
            submitted = st.form_submit_button("Create account", type="primary")

        if submitted:
            name = name.strip()
            email = email.strip().lower()
            validation_error = _valid_details(name, email)
            if validation_error:
                st.warning(validation_error)
            else:
                success, message = database.register_learner(name, email)
                if success:
                    learner = database.get_learner(name, email)
                    st.success(message)
                    if learner:
                        _start_session(learner)
                else:
                    st.error(message)

    st.divider()
    if st.button("Administrator sign in"):
        st.session_state.page = "admin_login"
        st.rerun()