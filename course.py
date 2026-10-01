import os
import tkinter as tk
from tkinter import messagebox

from navigation import Page
import database


class CourseWindow:

    def __init__(self, parent, learner_id=None):
        self.learner_id = learner_id

        self.window = Page(parent)
        self.window.title("5-Day Internet Basics Course")
        self.window.geometry("1100x720")
        self.window.configure(bg="#F7F4FF")

        # --------------------------------------------------
        # COURSE DATA
        # --------------------------------------------------
        self.course = {
            "Day 1": {
                "title": "🌐 Introduction to Internet",
                "color": "#2196F3",
                "subtitle": "Learn what the Internet is and how it helps us in daily life.",
                "content": """WHAT IS THE INTERNET?

The Internet is a worldwide network that connects millions of computers, phones and other devices.

It allows people to communicate, learn, work, shop and share information online.

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
• Online Shopping""",
                "points": [
                    "The Internet connects computers and devices all over the world.",
                    "It helps us communicate with people.",
                    "We can learn new things online.",
                    "We can work, shop and share information."
                ],
                "examples": "Google • YouTube • Wikipedia • Gmail • Online Shopping",
                "image": "day1_internet.png",
                "example_cards": [
                    ("🔎", "Google", "Used to search for information online."),
                    ("▶", "YouTube", "Used to watch videos and learn online."),
                    ("✉", "Gmail", "Used to send and receive emails."),
                    ("🛒", "Online Shopping", "Used to browse and buy products online.")
                ]
            },

            "Day 2": {
                "title": "🌍 Web Browsers",
                "color": "#00A896",
                "subtitle": "Learn how to open and use websites with a web browser.",
                "content": """WHAT IS A WEB BROWSER?

A web browser is software used to access and view websites on the Internet.

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

www.google.com""",
                "points": [
                    "A browser is used to access websites.",
                    "Chrome, Edge, Firefox and Safari are browsers.",
                    "A website address is typed into the address bar.",
                    "Press Enter to open the website."
                ],
                "examples": "Chrome • Edge • Firefox • Safari",
                "image": "day2_browser.png",
                "example_cards": [
                    ("🌐", "Chrome", "A popular web browser used to open websites."),
                    ("🌐", "Edge", "A web browser used to access websites."),
                    ("🌐", "Firefox", "A web browser for viewing websites."),
                    ("🌐", "Safari", "A web browser used on Apple devices.")
                ]
            },

            "Day 3": {
                "title": "🔍 Search Engines",
                "color": "#F4A261",
                "subtitle": "Learn how to search for useful information on the Internet.",
                "content": """WHAT IS A SEARCH ENGINE?

A search engine helps us find information on the Internet.

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

The search engine will show useful results.""",
                "points": [
                    "A search engine helps us find information.",
                    "Use simple and clear keywords.",
                    "Read the search results carefully.",
                    "Do not open suspicious results or links."
                ],
                "examples": "Google • Bing • Yahoo",
                "image": "day3_search.png",
                "example_cards": [
                    ("G", "Google", "A search engine used to find information."),
                    ("B", "Bing", "A search engine for finding web results."),
                    ("Y", "Yahoo", "A search engine and online information service."),
                    ("⌕", "Search Tip", "Use clear keywords such as: create an email account.")
                ]
            },

            "Day 4": {
                "title": "📧 Email",
                "color": "#E76F9A",
                "subtitle": "Learn how to send and receive messages using email.",
                "content": """WHAT IS EMAIL?

Email means Electronic Mail.

It allows us to send and receive messages through the Internet.

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

Never share your email password with anyone.""",
                "points": [
                    "Email means Electronic Mail.",
                    "Email can be used to send and receive messages.",
                    "Always check the receiver's email address.",
                    "Never share your email password."
                ],
                "examples": "Gmail • Outlook • Yahoo Mail",
                "image": "day4_email.png",
                "example_cards": [
                    ("✉", "Gmail", "An email service used to send and receive messages."),
                    ("✉", "Outlook", "An email service for messages and communication."),
                    ("✉", "Yahoo Mail", "An email service used for sending and receiving email."),
                    ("✓", "Before Send", "Check the receiver address and subject before sending.")
                ]
            },

            "Day 5": {
                "title": "🛡️ Internet Safety",
                "color": "#8E5CC2",
                "subtitle": "Learn how to stay safe and protect your personal information online.",
                "content": """WHAT IS INTERNET SAFETY?

Internet safety means using the Internet carefully and protecting our personal information.

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

Before clicking any unknown link, check whether it is safe.""",
                "points": [
                    "Never share OTPs or passwords.",
                    "Avoid unknown or suspicious links.",
                    "Use strong passwords and protect personal information.",
                    "Logout when using a public computer.",
                    "STOP • THINK • CHECK before clicking."
                ],
                "examples": "OTP • Password • Links • Personal Information",
                "image": "day5_safety.png",
                "example_cards": [
                    ("🔑", "Password", "Keep your password private and use a strong password."),
                    ("🔢", "OTP", "Never share an OTP with another person."),
                    ("🔗", "Unknown Link", "Do not click an unknown link before checking it."),
                    ("🛡", "Personal Info", "Protect personal information when using websites.")
                ]
            }
        }

        self.days = list(self.course.keys())
        self.current_day = 0
        self.image_refs = {}
        self.example_open = {}
        self.example_buttons = []
        self.example_messages = []

        try:
            self.completed_lessons = database.get_completed_lessons(self.learner_id)
        except Exception as error:
            print("Could not load lesson progress:", error)
            self.completed_lessons = []

        self.create_header()
        self.create_layout()
        self.show_day(0)

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------
    def create_header(self):
        header = tk.Frame(
            self.window,
            bg="#5B2C83",
            height=78
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📚  5-Day Internet Basics Course",
            font=("Arial", 23, "bold"),
            bg="#5B2C83",
            fg="white"
        ).pack(side="left", padx=25, pady=18)

        tk.Label(
            header,
            text="Learn • Practice • Complete",
            font=("Arial", 11, "bold"),
            bg="#5B2C83",
            fg="#EDE3FF"
        ).pack(side="right", padx=25)

    # --------------------------------------------------
    # MAIN LAYOUT
    # --------------------------------------------------
    def create_layout(self):
        main = tk.Frame(
            self.window,
            bg="#F7F4FF"
        )
        main.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=16
        )

        # ==================================================
        # LEFT SIDEBAR - FIXED
        # ==================================================
        left = tk.Frame(
            main,
            bg="white",
            width=245,
            highlightbackground="#DDD5EE",
            highlightthickness=1
        )
        left.pack(
            side="left",
            fill="y",
            padx=(0, 14)
        )
        left.pack_propagate(False)

        tk.Label(
            left,
            text="📅  COURSE DAYS",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#5B2C83"
        ).pack(pady=(18, 4))

        tk.Label(
            left,
            text="Learn step by step",
            font=("Arial", 10),
            bg="white",
            fg="#777777"
        ).pack()

        self.progress_label = tk.Label(
            left,
            text="0 / 5 Completed",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#555555"
        )
        self.progress_label.pack(pady=(12, 5))

        self.progress_bar_bg = tk.Frame(
            left,
            bg="#E5E5E5",
            height=12
        )
        self.progress_bar_bg.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )
        self.progress_bar_bg.pack_propagate(False)

        self.progress_bar = tk.Frame(
            self.progress_bar_bg,
            bg="#43A047",
            height=12
        )
        self.progress_bar.place(
            x=0,
            y=0,
            relheight=1,
            relwidth=0
        )

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
                text=day,
                font=("Arial", 11, "bold"),
                bg=colors[i],
                fg="white",
                activebackground=colors[i],
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                width=20,
                height=2,
                command=lambda index=i: self.select_day(index)
            )
            button.pack(
                pady=5,
                padx=14
            )
            self.day_buttons.append(button)

        tk.Label(
            left,
            text="💡 Tip\nRead the lesson and examples\nbefore completing the day.\n\nScroll down on the lesson\npage for more information.",
            font=("Arial", 9),
            bg="#F8F5FF",
            fg="#555555",
            justify="left",
            padx=10,
            pady=10
        ).pack(
            side="bottom",
            fill="x",
            padx=12,
            pady=14
        )

        # ==================================================
        # RIGHT SIDE - FULLY SCROLLABLE
        # ==================================================
        right_outer = tk.Frame(
            main,
            bg="white",
            highlightbackground="#DDD5EE",
            highlightthickness=1
        )
        right_outer.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.course_canvas = tk.Canvas(
            right_outer,
            bg="white",
            highlightthickness=0,
            borderwidth=0
        )
        self.course_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        course_scrollbar = tk.Scrollbar(
            right_outer,
            orient="vertical",
            command=self.course_canvas.yview
        )
        course_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.course_canvas.configure(
            yscrollcommand=course_scrollbar.set
        )

        self.scroll_frame = tk.Frame(
            self.course_canvas,
            bg="white"
        )

        self.canvas_window = self.course_canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw"
        )

        self.scroll_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.course_canvas.bind(
            "<Configure>",
            self.resize_scroll_frame
        )

        # Mouse wheel
        self.course_canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        self.scroll_frame.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        # ==================================================
        # CONTENT HEADER
        # ==================================================
        self.topic_title = tk.Label(
            self.scroll_frame,
            text="",
            font=("Arial", 21, "bold"),
            bg="white",
            fg="#5B2C83"
        )
        self.topic_title.pack(
            anchor="w",
            padx=22,
            pady=(15, 2)
        )

        self.subtitle_label = tk.Label(
            self.scroll_frame,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="#777777"
        )
        self.subtitle_label.pack(
            anchor="w",
            padx=23,
            pady=(0, 8)
        )

        # ==================================================
        # IMAGE + THEORY
        # ==================================================
        self.top_content = tk.Frame(
            self.scroll_frame,
            bg="white",
            height=320
        )
        self.top_content.pack(
            fill="x",
            padx=18,
            pady=4
        )
        self.top_content.pack_propagate(False)

        # IMAGE
        image_panel = tk.Frame(
            self.top_content,
            bg="#EEF7FF",
            width=300
        )
        image_panel.pack(
            side="right",
            fill="y",
            padx=(12, 0)
        )
        image_panel.pack_propagate(False)

        self.image_label = tk.Label(
            image_panel,
            text="",
            bg="#EEF7FF",
            fg="#777777"
        )
        self.image_label.pack(
            expand=True,
            padx=10,
            pady=10
        )

        # THEORY
        theory_panel = tk.Frame(
            self.top_content,
            bg="#FAFAFF"
        )
        theory_panel.pack(
            side="left",
            fill="both",
            expand=True
        )

        theory_scrollbar = tk.Scrollbar(theory_panel)
        theory_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.text = tk.Text(
            theory_panel,
            font=("Arial", 12),
            wrap="word",
            bg="#FAFAFF",
            fg="#333333",
            relief="flat",
            padx=18,
            pady=15,
            yscrollcommand=theory_scrollbar.set
        )
        self.text.pack(
            fill="both",
            expand=True
        )

        theory_scrollbar.config(
            command=self.text.yview
        )

        # ==================================================
        # SCROLL HINT
        # ==================================================
        tk.Label(
            self.scroll_frame,
            text="⬇ Scroll down for Key Points, Examples and Lesson Completion",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#7A5AA6"
        ).pack(
            pady=(3, 8)
        )

        # ==================================================
        # INFO CARDS
        # ==================================================
        cards = tk.Frame(
            self.scroll_frame,
            bg="white"
        )
        cards.pack(
            fill="x",
            padx=18,
            pady=(0, 8)
        )

        self.points_card = tk.Frame(
            cards,
            bg="#FFF8E7",
            highlightbackground="#F0E3B5",
            highlightthickness=1
        )
        self.points_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 6)
        )

        self.examples_card = tk.Frame(
            cards,
            bg="#EEF8F0",
            highlightbackground="#CFE5D2",
            highlightthickness=1
        )
        self.examples_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(6, 0)
        )

        tk.Label(
            self.points_card,
            text="💡 KEY POINTS",
            font=("Arial", 12, "bold"),
            bg="#FFF8E7",
            fg="#6A4A00"
        ).pack(
            anchor="w",
            padx=14,
            pady=(12, 6)
        )

        self.points_label = tk.Label(
            self.points_card,
            text="",
            font=("Arial", 10),
            bg="#FFF8E7",
            fg="#6A4A00",
            justify="left",
            anchor="nw",
            padx=14,
            pady=4,
            wraplength=400
        )
        self.points_label.pack(
            fill="both",
            expand=True,
            padx=2,
            pady=(0, 12)
        )

        tk.Label(
            self.examples_card,
            text="⭐ EXAMPLES  •  Click to reveal",
            font=("Arial", 12, "bold"),
            bg="#EEF8F0",
            fg="#27632A"
        ).pack(
            anchor="w",
            padx=14,
            pady=(12, 6)
        )

        self.example_grid = tk.Frame(
            self.examples_card,
            bg="#EEF8F0"
        )
        self.example_grid.pack(
            fill="x",
            padx=10,
            pady=(0, 12)
        )

        # ==================================================
        # NAVIGATION
        # ==================================================
        navigation = tk.Frame(
            self.scroll_frame,
            bg="white"
        )
        navigation.pack(
            fill="x",
            pady=(8, 16)
        )

        self.previous_button = tk.Button(
            navigation,
            text="⬅ Previous",
            font=("Arial", 11, "bold"),
            bg="#757575",
            fg="white",
            activebackground="#666666",
            relief="flat",
            cursor="hand2",
            width=15,
            command=self.previous_day
        )
        self.previous_button.pack(
            side="left",
            padx=18
        )

        self.complete_button = tk.Button(
            navigation,
            text="✓ Mark Day Complete",
            font=("Arial", 11, "bold"),
            bg="#43A047",
            fg="white",
            activebackground="#2E7D32",
            relief="flat",
            cursor="hand2",
            width=19,
            command=self.complete_current_day
        )
        self.complete_button.pack(
            side="left",
            expand=True
        )

        self.next_button = tk.Button(
            navigation,
            text="Next Day ➡",
            font=("Arial", 11, "bold"),
            bg="#5B2C83",
            fg="white",
            activebackground="#482168",
            relief="flat",
            cursor="hand2",
            width=15,
            command=self.next_day
        )
        self.next_button.pack(
            side="right",
            padx=18
        )

        # Make sure the page starts at top.
        self.course_canvas.yview_moveto(0)

    # --------------------------------------------------
    # SCROLLING
    # --------------------------------------------------
    def update_scroll_region(self, event=None):
        self.course_canvas.configure(
            scrollregion=self.course_canvas.bbox("all")
        )

    def resize_scroll_frame(self, event):
        self.course_canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )

    def on_mousewheel(self, event):
        try:
            self.course_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        except tk.TclError:
            pass

    # --------------------------------------------------
    # SELECT / SHOW DAY
    # --------------------------------------------------
    def select_day(self, index):
        self.show_day(index)

    def show_day(self, index):
        self.current_day = index
        day = self.days[index]
        information = self.course[day]

        self.topic_title.config(
            text=information["title"],
            fg=information["color"]
        )

        self.subtitle_label.config(
            text=information["subtitle"]
        )

        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, information["content"])
        self.text.config(state="disabled")
        self.text.yview_moveto(0)

        # Key points
        points_text = "\n".join(
            "✓ " + point
            for point in information["points"]
        )

        self.points_label.config(
            text=points_text
        )

        # Interactive examples
        self.build_example_cards(
            information.get("example_cards", [])
        )

        # Image
        image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets",
            "course",
            information["image"]
        )

        try:
            image = tk.PhotoImage(file=image_path)
            image = self.fit_image(
                image,
                280,
                250
            )

            self.image_refs[day] = image

            self.image_label.config(
                image=image,
                text=""
            )

        except Exception as error:
            print(
                "Could not load course image:",
                error
            )

            self.image_label.config(
                image="",
                text="🖼️\nCourse image\nnot available",
                font=("Arial", 14, "bold")
            )

        self.update_day_buttons()

        if index == 0:
            self.previous_button.config(
                state="disabled"
            )
        else:
            self.previous_button.config(
                state="normal"
            )

        if (index + 1) in self.completed_lessons:
            self.complete_button.config(
                text="✓ Day Completed",
                bg="#2E7D32"
            )
        else:
            self.complete_button.config(
                text="✓ Mark Day Complete",
                bg="#43A047"
            )

        if index == len(self.days) - 1:
            self.next_button.config(
                text="Finish Course ➜"
            )
        else:
            self.next_button.config(
                text="Next Day ➡"
            )

        # Reset scroll to the top whenever a new day is selected.
        self.course_canvas.yview_moveto(0)

        self.window.after_idle(
            self.update_scroll_region
        )

    # --------------------------------------------------
    # INTERACTIVE EXAMPLE CARDS
    # --------------------------------------------------
    def build_example_cards(self, examples):
        for widget in self.example_grid.winfo_children():
            widget.destroy()

        self.example_open = {}
        self.example_buttons = []
        self.example_messages = []

        # Four cards in one row on a wide screen.
        # Tkinter will keep them compact inside the scrollable page.
        for index, (icon, title, message) in enumerate(examples[:4]):
            self.example_open[index] = False

            card = tk.Frame(
                self.example_grid,
                bg="white",
                highlightbackground="#D4E6D6",
                highlightthickness=1
            )
            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=4,
                pady=4
            )

            self.example_grid.grid_columnconfigure(
                index,
                weight=1
            )

            tk.Label(
                card,
                text=icon,
                font=("Arial", 22, "bold"),
                bg="white",
                fg="#2E7D32"
            ).pack(pady=(8, 1))

            tk.Label(
                card,
                text=title,
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#333333"
            ).pack(pady=(0, 4))

            message_label = tk.Label(
                card,
                text="Click Show Example",
                font=("Arial", 9),
                bg="white",
                fg="#777777",
                wraplength=170,
                justify="center",
                height=2
            )
            message_label.pack(
                fill="x",
                padx=5,
                pady=(0, 5)
            )

            self.example_messages.append(
                (message_label, message)
            )

            button = tk.Button(
                card,
                text="🔍 Show Example",
                font=("Arial", 9, "bold"),
                bg="#2196F3",
                fg="white",
                activebackground="#1565C0",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                padx=7,
                pady=4,
                command=lambda i=index: self.toggle_example(i)
            )
            button.pack(
                padx=7,
                pady=(0, 9)
            )

            self.example_buttons.append(button)

        self.window.after_idle(
            self.update_scroll_region
        )

    def toggle_example(self, index):
        if index < 0 or index >= len(self.example_messages):
            return

        message_label, message = self.example_messages[index]

        if self.example_open[index]:
            message_label.config(
                text="Click Show Example"
            )

            self.example_buttons[index].config(
                text="🔍 Show Example",
                bg="#2196F3",
                activebackground="#1565C0"
            )

            self.example_open[index] = False

        else:
            message_label.config(
                text=message,
                fg="#27632A"
            )

            self.example_buttons[index].config(
                text="▲ Hide Example",
                bg="#2E7D32",
                activebackground="#1B5E20"
            )

            self.example_open[index] = True

        self.window.after_idle(
            self.update_scroll_region
        )

    # --------------------------------------------------
    # IMAGE RESIZE WITHOUT PILLOW
    # --------------------------------------------------
    def fit_image(self, image, max_width, max_height):
        width = image.width()
        height = image.height()

        factor = max(
            width / max_width,
            height / max_height
        )

        if factor <= 1:
            return image

        subsample = int(factor) + 1

        return image.subsample(
            subsample,
            subsample
        )

    # --------------------------------------------------
    # PROGRESS
    # --------------------------------------------------
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
        total = len(self.days)

        self.progress_label.config(
            text=f"{completed_count} / {total} Completed"
        )

        progress = (
            completed_count / total
            if total
            else 0
        )

        self.progress_bar.place_configure(
            relwidth=progress
        )

        for i, button in enumerate(
            self.day_buttons
        ):
            lesson_number = i + 1

            if lesson_number in self.completed_lessons:
                button.config(
                    text=f"✓ {self.days[i]}",
                    bg="#2E7D32"
                )
            else:
                button.config(
                    text=self.days[i],
                    bg=colors[i]
                )

            if i == self.current_day:
                button.config(
                    relief="sunken",
                    bd=3
                )
            else:
                button.config(
                    relief="flat",
                    bd=1
                )

    # --------------------------------------------------
    # MARK COMPLETE
    # --------------------------------------------------
    def mark_current_lesson_completed(self):
        if self.learner_id is None:
            messagebox.showwarning(
                "Progress Not Saved",
                "Student ID was not found, so lesson progress cannot be saved."
            )
            return False

        lesson_number = self.current_day + 1

        try:
            database.mark_lesson_completed(
                self.learner_id,
                lesson_number
            )

            self.completed_lessons = (
                database.get_completed_lessons(
                    self.learner_id
                )
            )

            self.update_day_buttons()

            return True

        except Exception as error:
            print(
                "Could not save lesson progress:",
                error
            )

            messagebox.showerror(
                "Error",
                "Could not save lesson progress."
            )

            return False

    def complete_current_day(self):
        already_completed = (
            self.current_day + 1
        ) in self.completed_lessons

        if already_completed:
            messagebox.showinfo(
                "Already Completed",
                f"✓ {self.days[self.current_day]} is already completed."
            )
            return

        if self.mark_current_lesson_completed():

            messagebox.showinfo(
                "Lesson Completed",
                f"🎉 {self.days[self.current_day]} completed!\n\n"
                "Your progress has been saved."
            )

            if self.current_day < len(self.days) - 1:
                self.show_day(
                    self.current_day + 1
                )
            else:
                messagebox.showinfo(
                    "Course Completed",
                    "🎉 Congratulations!\n\n"
                    "You have completed all 5 days of the Internet Basics Course!"
                )

    # --------------------------------------------------
    # NEXT DAY
    # --------------------------------------------------
    def next_day(self):
        current_completed = (
            self.current_day + 1
        ) in self.completed_lessons

        if not current_completed:
            saved = self.mark_current_lesson_completed()

            if not saved:
                return

        if self.current_day < len(self.days) - 1:
            self.show_day(
                self.current_day + 1
            )
        else:
            if len(self.completed_lessons) == len(self.days):
                messagebox.showinfo(
                    "Course Completed",
                    "🎉 Congratulations!\n\n"
                    "You have completed all 5 days of the Internet Basics Course!\n\n"
                    "Your learning progress has been saved."
                )

    # --------------------------------------------------
    # PREVIOUS DAY
    # --------------------------------------------------
    def previous_day(self):
        if self.current_day > 0:
            self.show_day(
                self.current_day - 1
            )
