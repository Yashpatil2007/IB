"""Streamlit learner-records table for administrators."""

import streamlit as st

import database


def render_records():
    st.title("Learner records")
    learners = database.get_all_learners()
    search = st.text_input("Search by learner name or email")
    rows = []

    for learner in learners:
        learner_id, name, email, course_started, created_at = learner
        if search and search.casefold() not in f"{name} {email}".casefold():
            continue
        statistics = database.get_quiz_statistics(learner_id)
        attempts = statistics.get("attempts", 0)
        best_percentage = statistics.get("best_percentage") or 0
        rows.append(
            {
                "ID": learner_id,
                "Name": name,
                "Email": email,
                "Course started": course_started or "",
                "Registered": created_at or "",
                "Quiz attempts": attempts,
                "Best score": f"{float(best_percentage):.0f}%" if attempts else "No quiz",
            }
        )

    st.metric("Learners shown", len(rows))
    if rows:
        st.dataframe(rows, hide_index=True, width="stretch")
    else:
        st.info("No learner records match this search.")