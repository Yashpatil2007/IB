"""Learner dashboard rendered with Streamlit."""

import streamlit as st

import database


def render_dashboard(user):
    st.title(f"Welcome, {user['name']}")
    st.caption("Continue your Internet learning journey.")

    course = database.get_course_progress(user["id"])
    quiz = database.get_quiz_statistics(user["id"])
    best_score = float(quiz.get("best_percentage") or 0)

    metric_columns = st.columns(3)
    metric_columns[0].metric(
        "Course progress",
        f"{course['completed_count']}/{course['total_lessons']} lessons",
    )
    metric_columns[1].metric("Best quiz score", f"{best_score:.0f}%")
    metric_columns[2].metric("Quiz attempts", quiz.get("attempts", 0))

    st.progress(
        course["percentage"] / 100,
        text=f"{course['percentage']:.0f}% course completed",
    )

    left, right = st.columns(2)
    with left:
        st.subheader("Your lessons")
        for number in range(1, course["total_lessons"] + 1):
            status = "Complete" if number in course["completed_lessons"] else "Not started"
            st.write(f"Day {number} · {status}")
        if st.button("Continue course", type="primary", width="stretch"):
            st.session_state.page = "course"
            st.rerun()

    with right:
        st.subheader("Your quiz")
        st.write(f"Latest score: {float(quiz.get('latest_percentage') or 0):.0f}%")
        if quiz.get("passed"):
            st.success("Certificate unlocked")
            if st.button("View certificate", width="stretch"):
                st.session_state.page = "certificate"
                st.rerun()
        else:
            st.info("Score at least 70% to unlock your certificate.")
        if st.button("Take quiz", width="stretch"):
            st.session_state.quiz_result = None
            st.session_state.page = "quiz"
            st.rerun()