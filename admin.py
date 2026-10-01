"""Streamlit administrator authentication and overview pages."""

import streamlit as st

import database


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def render_admin_login():
    st.title("Administrator sign in")
    st.caption("Authorized administrators only")

    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", type="primary")

    if submitted:
        if username.strip() == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.is_admin = True
            st.session_state.page = "admin"
            st.rerun()
        else:
            st.error("Invalid administrator username or password.")

    if st.button("Back to learner sign in"):
        st.session_state.page = "login"
        st.rerun()


def render_admin_dashboard():
    st.title("Administrator dashboard")
    st.caption("Learner activity and quiz performance")

    try:
        learners = database.get_all_learners()
        statistics = database.get_overall_quiz_statistics()
    except Exception as error:
        st.error(f"Could not load administrator data: {error}")
        return

    columns = st.columns(4)
    columns[0].metric("Learners", len(learners))
    columns[1].metric("Quiz attempts", statistics.get("attempts", 0))
    columns[2].metric("Passed attempts", statistics.get("passed", 0))
    columns[3].metric(
        "Average score",
        f"{float(statistics.get('average_percentage') or 0):.0f}%",
    )

    st.subheader("Recent learners")
    rows = [
        {
            "ID": learner[0],
            "Name": learner[1],
            "Email": learner[2],
            "Course started": learner[3] or "",
            "Registered": learner[4] or "",
        }
        for learner in learners
    ]
    if rows:
        st.dataframe(rows, hide_index=True, width="stretch")
    else:
        st.info("No learners have registered yet.")