import tkinter as tk
from tkinter import messagebox

from navigation import Page
from certificate import CertificateWindow
import database


class QuizWindow:

    def __init__(
        self,
        parent,
        student_name="Student",
        learner_id=None,
        on_pass=None,
        on_certificate=None
    ):

        self.student_name = student_name
        self.learner_id = learner_id
        self.on_pass = on_pass
        self.on_certificate = on_certificate

        self.window = Page(parent)
        self.window.title("Internet Basics Quiz")
        self.window.geometry("1000x700")
        self.window.minsize(800, 600)
        self.window.configure(bg="#F5F0FF")

        # ==================================================
        # QUESTIONS
        # ==================================================
        # Questions are kept from the existing quiz.py.

        self.questions = [
            {
                "question": "1. 🌐 What is the Internet?",
                "options": [
                    "A worldwide network connecting computers",
                    "A mobile application",
                    "A type of printer",
                    "A computer game"
                ],
                "answer": "A worldwide network connecting computers"
            },

            {
                "question": "2. 🌍 Which application is used to browse websites?",
                "options": [
                    "Calculator",
                    "Google Chrome",
                    "Camera",
                    "Notepad"
                ],
                "answer": "Google Chrome"
            },

            {
                "question": "3. 🔍 You want to find information about Mumbai. What should you use?",
                "options": [
                    "Music Player",
                    "Calculator",
                    "Paint",
                    "Search Engine"
                ],
                "answer": "Search Engine"
            },

            {
                "question": "4. 📧 What is Email mainly used for?",
                "options": [
                    "Taking photographs",
                    "Sending and receiving messages online",
                    "Playing offline games",
                    "Editing videos"
                ],
                "answer": "Sending and receiving messages online"
            },

            {
                "question": "5. 📩 In an email, where do you enter the receiver's email address?",
                "options": [
                    "To",
                    "Subject",
                    "Message",
                    "Attachment"
                ],
                "answer": "To"
            },

            {
                "question": "6. 📝 What should you write in the Subject of an email?",
                "options": [
                    "Your OTP",
                    "Your password",
                    "The main topic of the email",
                    "Your phone PIN"
                ],
                "answer": "The main topic of the email"
            },

            {
                "question": "7. 📎 You want to send a photo with an email. What can you use?",
                "options": [
                    "Attachment",
                    "Subject",
                    "Search Bar",
                    "Browser History"
                ],
                "answer": "Attachment"
            },

            {
                "question": "8. 🔐 Which action is safest while using the Internet?",
                "options": [
                    "Never share your OTP or password",
                    "Click every unknown link",
                    "Share your password with friends",
                    "Use the same password everywhere"
                ],
                "answer": "Never share your OTP or password"
            },

            {
                "question": "9. ⚠️ You receive a message saying 'You won a prize! Click this unknown link.' What should you do?",
                "options": [
                    "Give your OTP",
                    "Click immediately",
                    "Share it with friends",
                    "Avoid clicking the link"
                ],
                "answer": "Avoid clicking the link"
            },

            {
                "question": "10. 🔑 Which password is the strongest?",
                "options": [
                    "123456",
                    "password",
                    "N@ziya123!",
                    "abcdef"
                ],
                "answer": "N@ziya123!"
            }
        ]

        # One selected answer for every question.
        self.selected_answers = [""] * len(self.questions)

        self.colors = [
            "#2196F3",
            "#00A896",
            "#FF9800",
            "#E91E63",
            "#673AB7",
            "#009688",
            "#3F51B5",
            "#4CAF50",
            "#F44336",
            "#9C27B0"
        ]

        self.answer_buttons = []

        # Quiz progress UI
        self.progress_label = None
        self.progress_bar = None

        self.create_header()
        self.create_quiz_area()

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    # ==================================================
    # HEADER
    # ==================================================

    def create_header(self):

        header = tk.Frame(
            self.window,
            bg="#542C85",
            height=85
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="❓ Internet Basics Quiz",
            font=("Arial", 25, "bold"),
            bg="#542C85",
            fg="white"
        ).pack(pady=22)

    # ==================================================
    # QUIZ AREA
    # ==================================================

    def create_quiz_area(self):

        tk.Label(
            self.window,
            text=f"Good luck, {self.student_name}! 🍀",
            font=("Arial", 18, "bold"),
            bg="#F5F0FF",
            fg="#542C85"
        ).pack(pady=(12, 3))

        tk.Label(
            self.window,
            text=(
                "Click 'Choose Answer' on each question. "
                "The answer options will open in a popup."
            ),
            font=("Arial", 12),
            bg="#F5F0FF",
            fg="#666666"
        ).pack(pady=(0, 8))

        tk.Label(
            self.window,
            text=(
                "You need at least 70% (7 out of 10) to pass "
                "and receive your certificate."
            ),
            font=("Arial", 10, "bold"),
            bg="#F5F0FF",
            fg="#7A5AA6"
        ).pack(pady=(0, 6))

        # ==================================================
        # QUIZ PROGRESS
        # ==================================================
        progress_area = tk.Frame(
            self.window,
            bg="#F5F0FF"
        )
        progress_area.pack(
            fill="x",
            padx=22,
            pady=(0, 8)
        )

        self.progress_label = tk.Label(
            progress_area,
            text="Answered 0 / 10",
            font=("Arial", 10, "bold"),
            bg="#F5F0FF",
            fg="#542C85"
        )
        self.progress_label.pack(anchor="w")

        progress_bg = tk.Frame(
            progress_area,
            bg="#E3DCEF",
            height=10
        )
        progress_bg.pack(
            fill="x",
            pady=(5, 0)
        )
        progress_bg.pack_propagate(False)

        self.progress_bar = tk.Frame(
            progress_bg,
            bg="#00A896",
            height=10
        )
        self.progress_bar.place(
            x=0,
            y=0,
            relheight=1,
            relwidth=0
        )

        # ==================================================
        # SCROLLABLE QUESTION AREA
        # ==================================================

        container = tk.Frame(
            self.window,
            bg="#F5F0FF"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )

        self.canvas = tk.Canvas(
            container,
            bg="#F5F0FF",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.quiz_frame = tk.Frame(
            self.canvas,
            bg="#F5F0FF"
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.quiz_frame,
            anchor="nw"
        )

        self.quiz_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_frame
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Mouse wheel
        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

        for i, question in enumerate(self.questions):
            self.create_question_card(
                i,
                question
            )

        # ==================================================
        # BUTTON BAR
        # ==================================================

        button_frame = tk.Frame(
            self.window,
            bg="#F5F0FF"
        )

        button_frame.pack(
            fill="x",
            pady=10
        )

        tk.Button(
            button_frame,
            text="✅ Submit Quiz",
            font=("Arial", 13, "bold"),
            bg="#00A896",
            fg="white",
            activebackground="#00796B",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            command=self.submit_quiz
        ).pack(
            side="left",
            padx=15
        )

        tk.Button(
            button_frame,
            text="🔄 Restart",
            font=("Arial", 13, "bold"),
            bg="#FF9800",
            fg="white",
            activebackground="#EF6C00",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=15,
            height=2,
            command=self.restart_quiz
        ).pack(
            side="left",
            padx=15
        )

        tk.Button(
            button_frame,
            text="❌ Close",
            font=("Arial", 13, "bold"),
            bg="#E53935",
            fg="white",
            activebackground="#B71C1C",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=15,
            height=2,
            command=self.close_window
        ).pack(
            side="right",
            padx=15
        )

    # ==================================================
    # QUESTION CARD
    # ==================================================

    def create_question_card(
        self,
        index,
        question
    ):

        color = self.colors[index]

        card = tk.Frame(
            self.quiz_frame,
            bg="white",
            highlightbackground=color,
            highlightthickness=3
        )

        card.pack(
            fill="x",
            padx=10,
            pady=8
        )

        # Question heading
        tk.Label(
            card,
            text=question["question"],
            font=("Arial", 14, "bold"),
            bg=color,
            fg="white",
            anchor="w",
            padx=15,
            pady=10
        ).pack(fill="x")

        # Answer area
        answer_area = tk.Frame(
            card,
            bg="white"
        )

        answer_area.pack(
            fill="x",
            padx=18,
            pady=12
        )

        tk.Label(
            answer_area,
            text="Your answer:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#666666"
        ).pack(
            anchor="w"
        )

        row = tk.Frame(
            answer_area,
            bg="white"
        )

        row.pack(
            fill="x",
            pady=(5, 0)
        )

        answer_button = tk.Button(
            row,
            text="🔽 Choose Answer",
            font=("Arial", 11, "bold"),
            bg="#F1ECF8",
            fg="#542C85",
            activebackground="#E2D8F0",
            activeforeground="#542C85",
            relief="solid",
            bd=1,
            cursor="hand2",
            padx=15,
            pady=9,
            command=lambda q_index=index: self.open_option_popup(q_index)
        )

        answer_button.pack(
            side="left"
        )

        selected_label = tk.Label(
            row,
            text="No answer selected",
            font=("Arial", 10),
            bg="white",
            fg="#999999",
            anchor="w"
        )

        selected_label.pack(
            side="left",
            padx=15
        )

        self.answer_buttons.append(
            {
                "button": answer_button,
                "label": selected_label
            }
        )

        tk.Frame(
            card,
            bg="white",
            height=4
        ).pack()

    # ==================================================
    # OPTION POPUP
    # ==================================================

    def open_option_popup(self, question_index):

        question = self.questions[question_index]

        popup = tk.Toplevel(self.window)
        popup.title("Choose Your Answer")
        popup.geometry("560x430")
        popup.minsize(500, 380)
        popup.configure(bg="#F5F0FF")

        popup.transient(self.window)
        popup.grab_set()

        # Center popup
        popup.update_idletasks()

        parent_x = self.window.winfo_rootx()
        parent_y = self.window.winfo_rooty()
        parent_w = self.window.winfo_width()
        parent_h = self.window.winfo_height()

        popup_w = popup.winfo_width()
        popup_h = popup.winfo_height()

        x = parent_x + max((parent_w - popup_w) // 2, 0)
        y = parent_y + max((parent_h - popup_h) // 2, 0)

        popup.geometry(
            f"+{x}+{y}"
        )

        # Header
        header = tk.Frame(
            popup,
            bg="#542C85",
            height=70
        )
        header.pack(
            fill="x"
        )
        header.pack_propagate(False)

        tk.Label(
            header,
            text="💡 Choose an Option",
            font=("Arial", 19, "bold"),
            bg="#542C85",
            fg="white"
        ).pack(
            pady=18
        )

        # Question
        tk.Label(
            popup,
            text=question["question"],
            font=("Arial", 12, "bold"),
            bg="#F5F0FF",
            fg="#542C85",
            wraplength=500,
            justify="left"
        ).pack(
            anchor="w",
            padx=22,
            pady=(15, 8)
        )

        selected = self.selected_answers[question_index]

        for option_index, option in enumerate(
            question["options"]
        ):
            option_letter = chr(65 + option_index)

            is_selected = (
                selected == option
            )

            button = tk.Button(
                popup,
                text=f"{option_letter}.  {option}",
                font=("Arial", 11),
                bg="#B2DFDB" if is_selected else "white",
                fg="#004D40" if is_selected else "#333333",
                activebackground="#80CBC4",
                activeforeground="#004D40",
                relief="solid" if is_selected else "flat",
                bd=1,
                anchor="w",
                cursor="hand2",
                padx=15,
                pady=9,
                command=lambda opt=option: self.choose_popup_option(
                    question_index,
                    opt,
                    popup
                )
            )

            button.pack(
                fill="x",
                padx=22,
                pady=4
            )

        tk.Label(
            popup,
            text="Click an option to select it.",
            font=("Arial", 9),
            bg="#F5F0FF",
            fg="#777777"
        ).pack(
            pady=(8, 4)
        )

        tk.Button(
            popup,
            text="Cancel",
            font=("Arial", 10, "bold"),
            bg="#757575",
            fg="white",
            activebackground="#616161",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=12,
            command=popup.destroy
        ).pack(
            pady=(0, 12)
        )

        popup.protocol(
            "WM_DELETE_WINDOW",
            popup.destroy
        )

    def choose_popup_option(
        self,
        question_index,
        option,
        popup
    ):

        self.selected_answers[question_index] = option

        answer_info = self.answer_buttons[question_index]

        answer_info["button"].config(
            text="✅ Change Answer",
            bg="#B2DFDB",
            fg="#004D40",
            activebackground="#80CBC4",
            activeforeground="#004D40"
        )

        answer_info["label"].config(
            text=f"Selected: {option}",
            fg="#00695C"
        )

        self.update_progress()

        popup.destroy()

    # ==================================================
    # QUIZ PROGRESS
    # ==================================================
    def update_progress(self):
        answered = sum(
            1
            for answer in self.selected_answers
            if answer
        )

        total = len(self.questions)

        if self.progress_label:
            self.progress_label.config(
                text=f"Answered {answered} / {total}"
            )

        if self.progress_bar:
            progress = answered / total if total else 0
            self.progress_bar.place_configure(
                relwidth=progress
            )

    def show_result_popup(
        self,
        score,
        total_questions,
        percentage,
        result
    ):
        popup = tk.Toplevel(self.window)
        popup.title("Quiz Result")
        popup.geometry("520x470")
        popup.minsize(470, 430)
        popup.configure(bg="#F5F0FF")

        popup.transient(self.window)
        popup.grab_set()

        popup.update_idletasks()

        parent_x = self.window.winfo_rootx()
        parent_y = self.window.winfo_rooty()
        parent_w = self.window.winfo_width()
        parent_h = self.window.winfo_height()

        popup_w = popup.winfo_width()
        popup_h = popup.winfo_height()

        x = parent_x + max((parent_w - popup_w) // 2, 0)
        y = parent_y + max((parent_h - popup_h) // 2, 0)

        popup.geometry(f"+{x}+{y}")

        passed = result == "PASSED"
        header_color = "#2E7D32" if passed else "#E65100"
        title = "🎉 Quiz Completed!" if passed else "📚 Keep Learning!"

        header = tk.Frame(
            popup,
            bg=header_color,
            height=78
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=title,
            font=("Arial", 22, "bold"),
            bg=header_color,
            fg="white"
        ).pack(pady=20)

        tk.Label(
            popup,
            text=self.student_name,
            font=("Arial", 13, "bold"),
            bg="#F5F0FF",
            fg="#542C85"
        ).pack(pady=(18, 4))

        score_card = tk.Frame(
            popup,
            bg="white",
            highlightbackground="#DED4EA",
            highlightthickness=1
        )
        score_card.pack(
            fill="x",
            padx=28,
            pady=12
        )

        tk.Label(
            score_card,
            text=f"{score} / {total_questions}",
            font=("Arial", 32, "bold"),
            bg="white",
            fg=header_color
        ).pack(pady=(14, 0))

        tk.Label(
            score_card,
            text=f"{percentage:.0f}%",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#444444"
        ).pack()

        tk.Label(
            score_card,
            text="✅ PASSED" if passed else "❌ NOT PASSED",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=header_color
        ).pack(pady=(4, 14))

        if passed:
            tk.Label(
                popup,
                text=(
                    "You scored 70% or above.\n"
                    "Your certificate is ready."
                ),
                font=("Arial", 10),
                bg="#F5F0FF",
                fg="#555555",
                justify="center"
            ).pack(pady=(0, 10))

            tk.Button(
                popup,
                text="🏆 Continue to Certificate",
                font=("Arial", 11, "bold"),
                bg="#2E7D32",
                fg="white",
                activebackground="#1B5E20",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                width=26,
                height=2,
                command=lambda: self.continue_to_certificate(popup)
            ).pack(pady=5)

        else:
            tk.Label(
                popup,
                text=(
                    "You need at least 70% to pass.\n"
                    "Review the course and try again."
                ),
                font=("Arial", 10),
                bg="#F5F0FF",
                fg="#555555",
                justify="center"
            ).pack(pady=(0, 10))

            tk.Button(
                popup,
                text="🔄 Retry Quiz",
                font=("Arial", 11, "bold"),
                bg="#FF9800",
                fg="white",
                activebackground="#EF6C00",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                width=22,
                height=2,
                command=lambda: self.retry_from_result(popup)
            ).pack(pady=5)

        tk.Button(
            popup,
            text="Close",
            font=("Arial", 10, "bold"),
            bg="#757575",
            fg="white",
            activebackground="#616161",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=14,
            command=lambda: self.close_result_popup(popup)
        ).pack(pady=5)

        popup.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.close_result_popup(popup)
        )

    def close_result_popup(self, popup):
        try:
            popup.grab_release()
        except Exception:
            pass
        popup.destroy()

    def retry_from_result(self, popup):
        self.close_result_popup(popup)
        self.restart_quiz(show_message=False)

    def continue_to_certificate(self, popup):
        self.close_result_popup(popup)

        if self.on_pass:
            self.on_pass()

        host = self.window.master
        self.window.destroy_silently()

        if self.on_certificate:
            self.on_certificate()
        else:
            CertificateWindow(
                host,
                self.student_name,
                self.learner_id
            )

    # ==================================================
    # SCROLL
    # ==================================================

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_frame(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def mouse_scroll(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==================================================
    # SUBMIT QUIZ
    # ==================================================

    def submit_quiz(self):

        # Make sure every question has an answer.
        unanswered = [
            index + 1
            for index, answer in enumerate(
                self.selected_answers
            )
            if not answer
        ]

        if unanswered:

            messagebox.showwarning(
                "Incomplete Quiz",
                "Please answer all 10 questions before submitting.\n\n"
                f"Unanswered question(s): {', '.join(map(str, unanswered))}"
            )

            # Bring the user back to the first unanswered question.
            self.scroll_to_question(
                unanswered[0] - 1
            )

            return

        score = 0

        for index, question in enumerate(
            self.questions
        ):

            if (
                self.selected_answers[index]
                == question["answer"]
            ):
                score += 1

        total_questions = len(
            self.questions
        )

        percentage = (
            score / total_questions
        ) * 100

        if percentage >= 70:
            result = "PASSED"
        else:
            result = "FAILED"

        # Save attempt
        if self.learner_id is not None:
            database.add_quiz_attempt(
                self.learner_id,
                score,
                total_questions,
                percentage,
                result
            )

        self.show_result_popup(
            score,
            total_questions,
            percentage,
            result
        )

    # ==================================================
    # SCROLL TO QUESTION
    # ==================================================

    def scroll_to_question(
        self,
        question_index
    ):

        children = self.quiz_frame.winfo_children()

        if (
            question_index < 0
            or question_index >= len(children)
        ):
            return

        question_widget = children[
            question_index
        ]

        self.window.update_idletasks()

        y = question_widget.winfo_y()
        total_height = max(
            self.quiz_frame.winfo_height(),
            1
        )

        self.canvas.yview_moveto(
            y / total_height
        )

    # ==================================================
    # RESTART QUIZ
    # ==================================================

    def restart_quiz(self, show_message=True):

        self.selected_answers = [
            ""
            for _ in self.questions
        ]

        for answer_info in self.answer_buttons:

            answer_info["button"].config(
                text="🔽 Choose Answer",
                bg="#F1ECF8",
                fg="#542C85",
                activebackground="#E2D8F0",
                activeforeground="#542C85"
            )

            answer_info["label"].config(
                text="No answer selected",
                fg="#999999"
            )

        self.update_progress()
        self.canvas.yview_moveto(0)

        if show_message:
            messagebox.showinfo(
                "🔄 Quiz Restarted",
                "All answers have been cleared.\n\n"
                "Choose the answers again. Good luck! 🍀"
            )

    # ==================================================
    # CLOSE
    # ==================================================

    def close_window(self):

        try:
            self.canvas.unbind_all(
                "<MouseWheel>"
            )
        except Exception:
            pass

        self.window.destroy()
