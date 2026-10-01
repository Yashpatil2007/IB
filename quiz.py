"""Streamlit quiz form and SQLite score submission."""

import streamlit as st

import database


QUESTIONS = [
    ("What is the Internet?", ["A worldwide network connecting computers", "A mobile application", "A type of printer", "A computer game"], "A worldwide network connecting computers"),
    ("Which application is used to browse websites?", ["Calculator", "Google Chrome", "Camera", "Notepad"], "Google Chrome"),
    ("You want to find information about Mumbai. What should you use?", ["Music Player", "Calculator", "Paint", "Search Engine"], "Search Engine"),
    ("What is email mainly used for?", ["Taking photographs", "Sending and receiving messages online", "Playing offline games", "Editing videos"], "Sending and receiving messages online"),
    ("Where do you enter the receiver's email address?", ["To", "Subject", "Message", "Attachment"], "To"),
    ("What should you write in the subject of an email?", ["Your OTP", "Your password", "The main topic of the email", "Your phone PIN"], "The main topic of the email"),
    ("What can you use to send a photo with an email?", ["Attachment", "Subject", "Search Bar", "Browser History"], "Attachment"),
    ("Which action is safest while using the Internet?", ["Never share your OTP or password", "Click every unknown link", "Share your password with friends", "Use the same password everywhere"], "Never share your OTP or password"),
    ("A message says you won a prize and asks you to click an unknown link. What should you do?", ["Give your OTP", "Click immediately", "Share it with friends", "Avoid clicking the link"], "Avoid clicking the link"),
    ("Which password is the strongest?", ["123456", "password", "N@ziya123!", "abcdef"], "N@ziya123!"),
]


def _clear_answers():
    for index in range(len(QUESTIONS)):
        st.session_state.pop(f"quiz_answer_{index}", None)
    st.session_state.quiz_result = None


def render_quiz(user):
    st.title("Internet Basics Quiz")
    result = st.session_state.quiz_result

    if result:
        st.subheader("Quiz result")
        st.metric("Score", f"{result['score']} / {result['total']}")
        st.metric("Percentage", f"{result['percentage']:.0f}%")
        if result["passed"]:
            st.success("Passed. Your certificate is unlocked.")
            if st.button("Continue to certificate", type="primary"):
                st.session_state.page = "certificate"
                st.rerun()
        else:
            st.warning("You need at least 70% to pass. Review the course and try again.")
        if st.button("Try again"):
            _clear_answers()
            st.rerun()
        return

    st.caption("Answer all 10 questions. A score of 70% or higher is a pass.")
    with st.form("internet_basics_quiz"):
        answers = []
        for index, (question, options, _) in enumerate(QUESTIONS):
            answer = st.radio(
                f"{index + 1}. {question}",
                options,
                index=None,
                key=f"quiz_answer_{index}",
            )
            answers.append(answer)
        submitted = st.form_submit_button("Submit quiz", type="primary")

    if not submitted:
        return

    unanswered = [str(index + 1) for index, answer in enumerate(answers) if answer is None]
    if unanswered:
        st.warning(f"Answer every question before submitting. Unanswered: {', '.join(unanswered)}")
        return

    score = sum(answer == question[2] for answer, question in zip(answers, QUESTIONS))
    total = len(QUESTIONS)
    percentage = score / total * 100
    passed = percentage >= 70

    database.add_quiz_attempt(
        user["id"],
        score,
        total,
        percentage,
        "PASSED" if passed else "FAILED",
    )
    st.session_state.quiz_result = {
        "score": score,
        "total": total,
        "percentage": percentage,
        "passed": passed,
    }
    st.rerun()