"""Streamlit course page for the five Internet Basics lessons."""

from pathlib import Path

import streamlit as st

import database


LESSONS = [
    {
        "title": "Introduction to the Internet",
        "subtitle": "Learn what the Internet is and how it helps in daily life.",
        "image": "day1_internet.png",
        "content": """### What is the Internet?

The Internet is a worldwide network that connects computers, phones, and other devices. It helps people communicate, learn, work, shop, and share information online.

### Topics
- What the Internet is and how it connects devices
- Common uses and advantages
- Examples of online services

### Examples
Google, YouTube, Wikipedia, Gmail, and online shopping.""",
        "points": [
            "The Internet connects devices around the world.",
            "It helps us communicate and learn.",
            "People work, shop, and share information online.",
        ],
        "examples": [
            ("Google", "Search for information online."),
            ("YouTube", "Watch videos and learn online."),
            ("Gmail", "Send and receive email."),
            ("Online shopping", "Browse and buy products online."),
        ],
    },
    {
        "title": "Web Browsers",
        "subtitle": "Learn how to open and use websites with a browser.",
        "image": "day2_browser.png",
        "content": """### What is a web browser?

A web browser is software used to access and view websites on the Internet.

### Popular browsers
Google Chrome, Microsoft Edge, Mozilla Firefox, and Safari.

### How to open a website
1. Open a web browser.
2. Type the website address in the address bar.
3. Press Enter to open the website.

For example, type `www.google.com` to open Google.""",
        "points": [
            "A browser is used to access websites.",
            "Chrome, Edge, Firefox, and Safari are browsers.",
            "Type an address in the address bar and press Enter.",
        ],
        "examples": [
            ("Chrome", "A popular browser for opening websites."),
            ("Edge", "A browser for accessing websites."),
            ("Firefox", "A browser for viewing websites."),
            ("Safari", "A browser commonly used on Apple devices."),
        ],
    },
    {
        "title": "Search Engines",
        "subtitle": "Learn to find useful information on the Internet.",
        "image": "day3_search.png",
        "content": """### What is a search engine?

A search engine helps us find information on the Internet. Popular search engines include Google, Bing, and Yahoo.

### How to search
1. Open a search engine.
2. Type a clear question or keyword.
3. Press Enter and review the results.
4. Avoid suspicious results and links.

For example, search for `how to create an email account`.""",
        "points": [
            "Use clear keywords to find information.",
            "Read search results carefully.",
            "Do not open suspicious results or links.",
        ],
        "examples": [
            ("Google", "Search for information and websites."),
            ("Bing", "Find web pages and other results."),
            ("Yahoo", "Search and browse online information."),
            ("Search tip", "Use a specific phrase, such as create an email account."),
        ],
    },
    {
        "title": "Email",
        "subtitle": "Learn how to send and receive messages online.",
        "image": "day4_email.png",
        "content": """### What is email?

Email means Electronic Mail. It lets us send and receive messages through the Internet.

### Popular services
Gmail, Outlook, and Yahoo Mail.

### How to send an email
1. Sign in to your email account.
2. Click Compose.
3. Enter the recipient's email address and a subject.
4. Write your message and click Send.

Always check the address before sending, and never share your password.""",
        "points": [
            "Email means Electronic Mail.",
            "Email sends and receives messages.",
            "Check the recipient's address before sending.",
            "Never share your email password.",
        ],
        "examples": [
            ("Gmail", "Send and receive email messages."),
            ("Outlook", "An email and communication service."),
            ("Yahoo Mail", "Send and receive email messages."),
            ("Before sending", "Check the recipient address and subject."),
        ],
    },
    {
        "title": "Internet Safety",
        "subtitle": "Protect your personal information and stay safe online.",
        "image": "day5_safety.png",
        "content": """### What is Internet safety?

Internet safety means using the Internet carefully and protecting personal information.

### Important rules
- Never share your OTP or password.
- Avoid unknown links and online strangers.
- Use strong passwords and protect personal information.
- Log out when using a public computer.

Remember: **Stop, think, check** before clicking an unfamiliar link.""",
        "points": [
            "Never share OTPs or passwords.",
            "Avoid unknown or suspicious links.",
            "Protect personal information online.",
            "Log out when using a public computer.",
            "Stop, think, and check before clicking.",
        ],
        "examples": [
            ("Password", "Keep it private and choose a strong one."),
            ("OTP", "Never share an OTP with another person."),
            ("Unknown link", "Check it before opening, or do not click."),
            ("Personal information", "Share it only when a website is trusted."),
        ],
    },
]


def render_course(user):
    st.title("5-Day Internet Basics Course")
    completed = set(database.get_completed_lessons(user["id"]))
    progress = len(completed) / len(LESSONS)
    st.progress(progress, text=f"{len(completed)} of {len(LESSONS)} lessons completed")

    if "course_day_selection" not in st.session_state:
        st.session_state.course_day_selection = st.session_state.get("course_day", 1)
    day_number = st.selectbox(
        "Choose a lesson",
        options=range(1, len(LESSONS) + 1),
        format_func=lambda value: f"Day {value}: {LESSONS[value - 1]['title']}",
        key="course_day_selection",
    )
    st.session_state.course_day = day_number
    lesson = LESSONS[day_number - 1]

    st.subheader(lesson["title"])
    st.caption(lesson["subtitle"])
    content_columns = st.columns([2, 1])
    with content_columns[0]:
        st.markdown(lesson["content"])
    with content_columns[1]:
        image_path = Path(__file__).parent / "assets" / "course" / lesson["image"]
        if image_path.is_file():
            st.image(str(image_path), width="stretch")

    st.markdown("#### Key points")
    for point in lesson["points"]:
        st.markdown(f"- {point}")

    st.markdown("#### Examples")
    example_columns = st.columns(2)
    for index, (title, description) in enumerate(lesson["examples"]):
        with example_columns[index % 2]:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(description)

    already_completed = day_number in completed
    if already_completed:
        st.success("This lesson is complete.")
    elif st.button("Mark lesson complete", type="primary"):
        if database.mark_lesson_completed(user["id"], day_number):
            st.success("Lesson progress saved.")
            st.rerun()
        else:
            st.error("Could not save this lesson's progress.")