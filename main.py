"""Streamlit entry point for Internet Basics Learning System."""

from pathlib import Path

import streamlit as st

import admin
import certificate
import course
import dashboard
import login
import navigation
import quiz
import records


st.set_page_config(
    page_title="Internet Basics Learning System",
    page_icon="🌐",
    layout="wide",
)


def load_stylesheet():
    stylesheet = Path(__file__).with_name("style.css")
    st.markdown(
        f"<style>{stylesheet.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


load_stylesheet()
navigation.initialize_state()


def render_sidebar():
    user = st.session_state.user
    is_admin = st.session_state.is_admin

    if not user and not is_admin:
        return

    with st.sidebar:
        st.title("Internet Basics")
        if user:
            st.caption(f"Signed in as {user['name']}")
            pages = (
                ("Overview", "dashboard"),
                ("Course", "course"),
                ("Quiz", "quiz"),
                ("Certificate", "certificate"),
            )
        else:
            st.caption("Administrator")
            pages = (("Overview", "admin"), ("Learner records", "records"))

        for label, page in pages:
            if st.button(label, key=f"nav_{page}", width="stretch"):
                st.session_state.page = page
                st.rerun()

        st.divider()
        if st.button("Sign out", key="sign_out", width="stretch"):
            navigation.logout()


def render_current_page():
    page = st.session_state.page
    user = st.session_state.user
    is_admin = st.session_state.is_admin

    if page == "login":
        login.render_login()
    elif page == "admin_login":
        admin.render_admin_login()
    elif user and page == "dashboard":
        dashboard.render_dashboard(user)
    elif user and page == "course":
        course.render_course(user)
    elif user and page == "quiz":
        quiz.render_quiz(user)
    elif user and page == "certificate":
        certificate.render_certificate(user)
    elif is_admin and page == "admin":
        admin.render_admin_dashboard()
    elif is_admin and page == "records":
        records.render_records()
    else:
        st.session_state.page = "login"
        st.rerun()


render_sidebar()
render_current_page()