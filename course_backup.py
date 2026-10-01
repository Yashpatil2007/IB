import tkinter as tk
from tkinter import messagebox

from navigation import Page
import database


class CourseWindow:

    def __init__(self, parent, learner_id=None):

        # Student ID from the logged-in user
        self.learner_id = learner_id

        self.window = Page(parent)

        self.window.title(
            "5-Day Internet Basics Course"
        )

        self.window.geometry(
            "1000x700"
        )

        self.window.configure(
            bg="#F7F4FF"
        )

        # ==================================================
        # COURSE DATA
        # ==================================================

        self.course = {

            "Day 1": {
                "title": "🌐 Introduction to Internet",
                "color": "#2196F3",

                "content": """
WHAT IS THE INTERNET?

The Internet is a worldwide network that connects
millions of computers, phones and other devices.

It allows people to communicate, learn, work,
shop and share information online.

TOPICS COVERED

✓ What is Internet?
✓ Uses of Internet
✓ Advantages of Internet
✓ Examples of Internet Services

EXAMPLES

• Google
• YouTube
• Wikipedia
• Gmail
• Online Shopping
"""
            },

            "Day 2": {
                "title": "🌍 Web Browsers",
                "color": "#00A896",

                "content": """
WHAT IS A WEB BROWSER?

A web browser is software used to access
and view websites on the Internet.

POPULAR WEB BROWSERS

✓ Google Chrome
✓ Microsoft Edge
✓ Mozilla Firefox
✓ Safari

HOW TO OPEN A WEBSITE

1. Open a web browser.

2. Type the website address.

3. Press Enter.

4. The website will open.

EXAMPLE

To open Google, type:

www.google.com
"""
            },

            "Day 3": {
                "title": "🔍 Search Engines",
                "color": "#F4A261",

                "content": """
WHAT IS A SEARCH ENGINE?

A search engine helps us find information
on the Internet.

POPULAR SEARCH ENGINES

✓ Google
✓ Bing
✓ Yahoo

HOW TO SEARCH

1. Open a search engine.

2. Type your question or keyword.

3. Press Enter.

4. Read the search results.

EXAMPLE

Search:

"How to create an email account?"

The search engine will show useful results.
"""
            },

            "Day 4": {
                "title": "📧 Email",
                "color": "#E76F9A",

                "content": """
WHAT IS EMAIL?

Email means Electronic Mail.

It allows us to send and receive messages
through the Internet.

POPULAR EMAIL SERVICES

✓ Gmail
✓ Outlook
✓ Yahoo Mail

HOW TO SEND AN EMAIL

1. Login to your email account.

2. Click Compose.

3. Enter the receiver's email address.

4. Enter the Subject.

5. Write your Message.

6. Click Send.

IMPORTANT

Never share your email password with anyone.
"""
            },

            "Day 5": {
                "title": "🛡️ Internet Safety",
                "color": "#8E5CC2",

                "content": """
WHAT IS INTERNET SAFETY?

Internet safety means using the Internet
carefully and protecting our personal information.

IMPORTANT SAFETY RULES

✓ Never share your OTP.

✓ Never share your password.

✓ Avoid unknown links.

✓ Use strong passwords.

✓ Do not share personal information.

✓ Logout from public computers.

✓ Be careful with online strangers.

✓ Think before clicking.

REMEMBER

STOP • THINK • CHECK

Before clicking any unknown link,
check whether it is safe.
"""
            }
        }

        self.days = list(
            self.course.keys()
        )

        self.current_day = 0

        # ==================================================
        # LOAD EXISTING PROGRESS
        # ==================================================

        try:

            self.completed_lessons = (
                database.get_completed_lessons(
                    self.learner_id
                )
            )

        except Exception as error:

            print(
                "Could not load lesson progress:",
                error
            )

            self.completed_lessons = []

        # ==================================================
        # CREATE UI
        # ==================================================

        self.create_header()

        self.create_layout()

        self.show_day(0)

    # ==================================================
    # HEADER
    # ==================================================

    def create_header(self):

        header = tk.Frame(
            self.window,
            bg="#5B2C83",
            height=90
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        title = tk.Label(
            header,
            text="📚 5-Day Internet Basics Course",
            font=("Arial", 24, "bold"),
            bg="#5B2C83",
            fg="white"
        )

        title.pack(
            pady=25
        )

    # ==================================================
    # MAIN LAYOUT
    # ==================================================

    def create_layout(self):

        main = tk.Frame(
            self.window,
            bg="#F7F4FF"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ==================================================
        # LEFT SIDE
        # ==================================================

        left = tk.Frame(
            main,
            bg="white",
            width=260
        )

        left.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        left.pack_propagate(
            False
        )

        tk.Label(
            left,
            text="📅 COURSE DAYS",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#5B2C83"
        ).pack(
            pady=(18, 5)
        )

        # Progress label

        self.progress_label = tk.Label(
            left,
            text="0 / 5 Completed",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#777777"
        )

        self.progress_label.pack(
            pady=(0, 12)
        )

        # Day buttons

        self.day_buttons = []

        colors = [
            "#2196F3",
            "#00A896",
            "#F4A261",
            "#E76F9A",
            "#8E5CC2"
        ]

        for i, day in enumerate(self.days):

            button = tk.Button(
                left,
                text="",
                font=("Arial", 12, "bold"),
                bg=colors[i],
                fg="white",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                width=20,
                height=2,

                command=lambda index=i:
                    self.select_day(index)
            )

            button.pack(
                pady=6,
                padx=15
            )

            self.day_buttons.append(
                button
            )

        # ==================================================
        # RIGHT SIDE
        # ==================================================

        right = tk.Frame(
            main,
            bg="white"
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Topic title

        self.topic_title = tk.Label(
            right,
            text="",
            font=("Arial", 21, "bold"),
            bg="white",
            fg="#5B2C83"
        )

        self.topic_title.pack(
            pady=(20, 10)
        )

        # Lesson text

        text_frame = tk.Frame(
            right,
            bg="white"
        )

        text_frame.pack(
            fill="both",
            expand=True,
            padx=20
        )

        scrollbar = tk.Scrollbar(
            text_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.text = tk.Text(
            text_frame,
            font=("Arial", 13),
            wrap="word",
            bg="#FAFAFF",
            fg="#333333",
            relief="flat",
            padx=20,
            pady=20,
            yscrollcommand=scrollbar.set
        )

        self.text.pack(
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.text.yview
        )

        # ==================================================
        # NAVIGATION
        # ==================================================

        navigation = tk.Frame(
            right,
            bg="white"
        )

        navigation.pack(
            fill="x",
            pady=15
        )

        # Previous

        self.previous_button = tk.Button(
            navigation,
            text="⬅ Previous",
            font=("Arial", 11, "bold"),
            bg="#757575",
            fg="white",
            relief="flat",
            cursor="hand2",
            width=15,
            command=self.previous_day
        )

        self.previous_button.pack(
            side="left",
            padx=20
        )

        # Next

        self.next_button = tk.Button(
            navigation,
            text="Next ➡",
            font=("Arial", 11, "bold"),
            bg="#43A047",
            fg="white",
            relief="flat",
            cursor="hand2",
            width=15,
            command=self.next_day
        )

        self.next_button.pack(
            side="right",
            padx=20
        )

        # Close

        close_button = tk.Button(
            navigation,
            text="❌ Close",
            font=("Arial", 11, "bold"),
            bg="#E63946",
            fg="white",
            relief="flat",
            cursor="hand2",
            width=12,
            command=self.window.destroy
        )

        close_button.pack(
            pady=5
        )

    # ==================================================
    # SELECT DAY
    # ==================================================

    def select_day(self, index):

        self.show_day(
            index
        )

    # ==================================================
    # SHOW DAY
    # ==================================================

    def show_day(self, index):

        self.current_day = index

        day = self.days[index]

        information = self.course[day]

        # ------------------------------------------------
        # TITLE
        # ------------------------------------------------

        self.topic_title.config(
            text=information["title"],
            fg=information["color"]
        )

        # ------------------------------------------------
        # CONTENT
        # ------------------------------------------------

        self.text.delete(
            "1.0",
            tk.END
        )

        self.text.insert(
            tk.END,
            information["content"]
        )

        # ------------------------------------------------
        # UPDATE DAY BUTTONS
        # ------------------------------------------------

        self.update_day_buttons()

        # ------------------------------------------------
        # PREVIOUS
        # ------------------------------------------------

        if index == 0:

            self.previous_button.config(
                state="disabled"
            )

        else:

            self.previous_button.config(
                state="normal"
            )

        # ------------------------------------------------
        # NEXT
        # ------------------------------------------------

        if index == len(self.days) - 1:

            if (index + 1) in self.completed_lessons:

                self.next_button.config(
                    text="✓ Completed",
                    bg="#2E7D32"
                )

            else:

                self.next_button.config(
                    text="✓ Complete Course",
                    bg="#43A047"
                )

        else:

            if (index + 1) in self.completed_lessons:

                self.next_button.config(
                    text="✓ Completed • Next ➡",
                    bg="#2E7D32"
                )

            else:

                self.next_button.config(
                    text="Complete & Next ➡",
                    bg="#43A047"
                )

    # ==================================================
    # UPDATE DAY BUTTONS
    # ==================================================

    def update_day_buttons(self):

        colors = [
            "#2196F3",
            "#00A896",
            "#F4A261",
            "#E76F9A",
            "#8E5CC2"
        ]

        completed_count = len(
            self.completed_lessons
        )

        self.progress_label.config(
            text=(
                f"{completed_count} / "
                f"{len(self.days)} Completed"
            )
        )

        for i, button in enumerate(
            self.day_buttons
        ):

            lesson_number = i + 1

            if lesson_number in self.completed_lessons:

                button.config(
                    text=f"✓ {self.days[i]}",
                    bg="#2E7D32",
                    relief="flat"
                )

            else:

                button.config(
                    text=self.days[i],
                    bg=colors[i],
                    relief="flat"
                )

            # Highlight current lesson

            if i == self.current_day:

                button.config(
                    relief="sunken",
                    bd=3
                )

            else:

                button.config(
                    bd=1
                )

    # ==================================================
    # MARK CURRENT LESSON COMPLETE
    # ==================================================

    def mark_current_lesson_completed(self):

        if self.learner_id is None:

            return False

        lesson_number = (
            self.current_day + 1
        )

        try:

            database.mark_lesson_completed(
                self.learner_id,
                lesson_number
            )

            # Refresh local progress

            self.completed_lessons = (
                database.get_completed_lessons(
                    self.learner_id
                )
            )

            return True

        except Exception as error:

            print(
                "Could not save lesson progress:",
                error
            )

            return False

    # ==================================================
    # NEXT DAY
    # ==================================================

    def next_day(self):

        # Mark current lesson completed

        self.mark_current_lesson_completed()

        # ------------------------------------------------
        # NEXT LESSON
        # ------------------------------------------------

        if self.current_day < len(self.days) - 1:

            self.show_day(
                self.current_day + 1
            )

        else:

            # Course complete

            if (
                len(self.completed_lessons)
                == len(self.days)
            ):

                messagebox.showinfo(
                    "Course Completed",
                    "🎉 Congratulations!\n\n"
                    "You have completed all 5 days "
                    "of the Internet Basics Course!\n\n"
                    "Your learning progress has "
                    "been saved."
                )

            else:

                messagebox.showinfo(
                    "Lesson Completed",
                    "✓ Day 5 has been completed."
                )

    # ==================================================
    # PREVIOUS DAY
    # ==================================================

    def previous_day(self):

        if self.current_day > 0:

            self.show_day(
                self.current_day - 1
            )