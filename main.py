import sqlite3
import tkinter as tk
from tkinter import messagebox

from course import CourseWindow
from quiz import QuizWindow
from login import LoginWindow
from admin import AdminLoginWindow
from navigation import PageHost
import certificate
import database


BG = "#F5F0FF"
PURPLE = "#542C85"
CARD_BG = "#FFFFFF"
TEXT = "#2E2E2E"
MUTED = "#777777"
GREEN = "#2E7D32"


class InternetBasicsApp:
    """
    Main application controller.

    Flow:
        Login -> Dashboard -> Course / Quiz / Certificate / Admin

    The dashboard shows learner-specific course and quiz progress.
    """

    def __init__(self, root):
        self.root = root

        self.root.title("Internet Basics Learning System")
        self.root.configure(bg=BG)

        self.set_window_size()

        # ---------- learner information ----------
        self.student_name = ""
        self.student_email = ""
        self.learner_id = None
        self.quiz_passed_this_login = False

        # ---------- top bar + page host ----------
        self.create_app_bar()

        self.host = PageHost(
            self.root,
            on_close=self.show_home,
            bg=BG
        )
        self.host.pack(fill="both", expand=True)

        self.show_login()

    # ==================================================
    # WINDOW
    # ==================================================

    def set_window_size(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        width = min(1180, screen_w - 40)
        height = min(820, screen_h - 70)

        x = max((screen_w - width) // 2, 0)
        y = max((screen_h - height) // 2 - 20, 0)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(980, 650)

    # ==================================================
    # TOP BAR
    # ==================================================

    def create_app_bar(self):
        bar = tk.Frame(
            self.root,
            bg=PURPLE,
            height=64
        )
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(
            bar,
            text="🌐 Internet Basics Learning System",
            font=("Arial", 20, "bold"),
            bg=PURPLE,
            fg="white"
        ).pack(side="left", padx=24)

        self.nav = tk.Frame(bar, bg=PURPLE)

        self.user_label = tk.Label(
            self.nav,
            text="",
            font=("Arial", 11, "bold"),
            bg=PURPLE,
            fg="#E8DFFF"
        )
        self.user_label.pack(side="left", padx=(0, 14))

        for text, command in (
            ("🏠 Home", self.show_home),
            ("🚪 Logout", self.logout),
        ):
            tk.Button(
                self.nav,
                text=text,
                font=("Arial", 10, "bold"),
                bg="#7B4BB3",
                fg="white",
                activebackground="#6A3CA0",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                padx=12,
                pady=5,
                command=command
            ).pack(side="left", padx=4)

    def show_nav(self, visible):
        if visible:
            self.user_label.config(text=f"👤 {self.student_name}")
            self.nav.pack(side="right", padx=20)
        else:
            self.nav.pack_forget()

    # ==================================================
    # LOGIN / LOGOUT
    # ==================================================

    def show_login(self):
        self.host.clear()
        self.show_nav(False)

        LoginWindow(
            self.host,
            self.login_success,
            self.registration_success
        )

    def registration_success(self, name, email):
        self.student_name = name
        self.student_email = email
        self.quiz_passed_this_login = False

        learner = database.get_learner(name, email)
        self.learner_id = learner[0] if learner else None

        self.show_home()

    def login_success(self, name, email):
        self.student_name = name
        self.student_email = email
        self.quiz_passed_this_login = False

        database.add_learner(name, email)

        learner = database.get_learner(name, email)
        self.learner_id = learner[0] if learner else None

        self.show_home()

    def logout(self):
        if not messagebox.askyesno(
            "Logout",
            "Do you want to log out?"
        ):
            return

        self.student_name = ""
        self.student_email = ""
        self.learner_id = None
        self.quiz_passed_this_login = False

        self.show_login()

    # ==================================================
    # DASHBOARD DATA
    # ==================================================

    def get_progress_data(self):
        """
        Returns:
            completed_count,
            total_lessons,
            completed_lessons,
            percentage
        """

        total_lessons = 5
        completed_lessons = []

        if self.learner_id is None:
            return 0, total_lessons, [], 0

        # Prefer functions from the updated database.py.
        try:
            completed_lessons = database.get_completed_lessons(
                self.learner_id
            )
        except Exception:
            completed_lessons = []

        # Make sure progress numbers are safe.
        completed_lessons = sorted(
            set(
                int(x)
                for x in completed_lessons
                if str(x).isdigit()
            )
        )

        try:
            progress = database.get_course_progress(
                self.learner_id
            )

            # Common supported forms:
            # (completed, total)
            # {"completed": ..., "total": ...}
            if isinstance(progress, (tuple, list)) and len(progress) >= 2:
                completed_count = int(progress[0])
                total_lessons = int(progress[1])
            elif isinstance(progress, dict):
                completed_count = int(
                    progress.get(
                        "completed",
                        progress.get("completed_count", len(completed_lessons))
                    )
                )
                total_lessons = int(
                    progress.get("total", 5)
                )
            else:
                completed_count = len(completed_lessons)
        except Exception:
            completed_count = len(completed_lessons)

        total_lessons = max(total_lessons, 5)
        completed_count = min(
            max(completed_count, 0),
            total_lessons
        )

        percentage = (
            round((completed_count / total_lessons) * 100)
            if total_lessons else 0
        )

        return (
            completed_count,
            total_lessons,
            completed_lessons,
            percentage
        )

    def get_quiz_data(self):
        """
        Returns:
            attempts,
            best_percentage,
            latest_percentage,
            latest_result
        """

        if self.learner_id is None:
            return 0, None, None, None

        attempts = 0
        best_percentage = None
        latest_percentage = None
        latest_result = None

        # Prefer updated database.py helper.
        try:
            stats = database.get_quiz_statistics(
                self.learner_id
            )

            if isinstance(stats, dict):
                attempts = int(stats.get("attempts", 0) or 0)
                best_percentage = stats.get(
                    "best_percentage",
                    stats.get("best_score")
                )
                latest_percentage = stats.get(
                    "latest_percentage",
                    stats.get("latest_score")
                )
                latest_result = stats.get("latest_result")
                return (
                    attempts,
                    best_percentage,
                    latest_percentage,
                    latest_result
                )

            if isinstance(stats, (tuple, list)):
                values = list(stats)
                if len(values) >= 1:
                    attempts = int(values[0] or 0)
                if len(values) >= 2:
                    best_percentage = values[1]
                if len(values) >= 3:
                    latest_percentage = values[2]
                if len(values) >= 4:
                    latest_result = values[3]
                return (
                    attempts,
                    best_percentage,
                    latest_percentage,
                    latest_result
                )
        except Exception:
            pass

        # Fallback: read quiz_attempts directly.
        try:
            connection = database.connect_database()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    MAX(percentage)
                FROM quiz_attempts
                WHERE learner_id = ?
                """,
                (self.learner_id,)
            )
            row = cursor.fetchone()

            attempts = int(row[0] or 0)
            best_percentage = row[1]

            cursor.execute(
                """
                SELECT percentage, result
                FROM quiz_attempts
                WHERE learner_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (self.learner_id,)
            )
            latest = cursor.fetchone()

            if latest:
                latest_percentage = latest[0]
                latest_result = latest[1]

            connection.close()

        except Exception:
            pass

        return (
            attempts,
            best_percentage,
            latest_percentage,
            latest_result
        )

    # ==================================================
    # SMALL UI HELPERS
    # ==================================================

    def make_stat_card(
        self,
        parent,
        title,
        value,
        subtitle,
        accent
    ):
        card = tk.Frame(
            parent,
            bg=CARD_BG,
            highlightbackground="#E2DAF0",
            highlightthickness=1,
            padx=18,
            pady=14
        )

        tk.Frame(
            card,
            bg=accent,
            width=5
        ).place(
            x=0,
            y=0,
            relheight=1
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            bg=CARD_BG,
            fg=MUTED
        ).pack(anchor="w")

        tk.Label(
            card,
            text=value,
            font=("Arial", 24, "bold"),
            bg=CARD_BG,
            fg=accent
        ).pack(anchor="w", pady=(3, 0))

        tk.Label(
            card,
            text=subtitle,
            font=("Arial", 9),
            bg=CARD_BG,
            fg="#666666"
        ).pack(anchor="w")

        return card

    def make_section_card(self, parent, title):
        card = tk.Frame(
            parent,
            bg=CARD_BG,
            highlightbackground="#E2DAF0",
            highlightthickness=1
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 14, "bold"),
            bg=CARD_BG,
            fg=PURPLE
        ).pack(anchor="w", padx=18, pady=(14, 8))

        return card

    # ==================================================
    # HOME / DASHBOARD
    # ==================================================

    def show_home(self):
        if not self.student_name:
            self.show_login()
            return

        self.host.clear()
        self.show_nav(True)

        completed_count, total_lessons, completed_lessons, progress_percent = (
            self.get_progress_data()
        )

        attempts, best_percentage, latest_percentage, latest_result = (
            self.get_quiz_data()
        )

        body = tk.Frame(
            self.host,
            bg=BG
        )
        body.pack(fill="both", expand=True)

        # ---------------- welcome ----------------
        welcome = tk.Frame(body, bg=BG)
        welcome.pack(fill="x", padx=28, pady=(20, 8))

        tk.Label(
            welcome,
            text=f"Welcome, {self.student_name}! 👋",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=PURPLE
        ).pack(anchor="w")

        tk.Label(
            welcome,
            text=(
                "Continue your Internet learning journey. "
                "Complete all 5 lessons and then take the quiz."
            ),
            font=("Arial", 11),
            bg=BG,
            fg="#555555"
        ).pack(anchor="w", pady=(3, 0))

        # ---------------- stat cards ----------------
        stats = tk.Frame(body, bg=BG)
        stats.pack(fill="x", padx=28, pady=(6, 12))

        course_card = self.make_stat_card(
            stats,
            "COURSE PROGRESS",
            f"{completed_count}/{total_lessons}",
            f"{progress_percent}% completed",
            "#2196F3"
        )
        course_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        best_text = (
            f"{float(best_percentage):.0f}%"
            if best_percentage is not None
            else "--"
        )

        best_card = self.make_stat_card(
            stats,
            "BEST QUIZ SCORE",
            best_text,
            "No attempt yet" if attempts == 0 else "Highest recorded score",
            "#7B4BB3"
        )
        best_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=4
        )

        attempt_card = self.make_stat_card(
            stats,
            "QUIZ ATTEMPTS",
            str(attempts),
            "Try again to improve your score",
            "#00A896"
        )
        attempt_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        # ---------------- lower content ----------------
        content = tk.Frame(body, bg=BG)
        content.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(0, 14)
        )

        # LEFT: course progress
        progress_card = self.make_section_card(
            content,
            "📚 Your Course Progress"
        )
        progress_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        progress_bar_bg = tk.Frame(
            progress_card,
            bg="#E7E2EF",
            height=16
        )
        progress_bar_bg.pack(
            fill="x",
            padx=18,
            pady=(2, 12)
        )
        progress_bar_bg.pack_propagate(False)

        fill = tk.Frame(
            progress_bar_bg,
            bg="#43A047",
            height=16
        )
        fill.place(
            x=0,
            y=0,
            relheight=1,
            relwidth=(progress_percent / 100)
        )

        tk.Label(
            progress_card,
            text=f"{completed_count} of {total_lessons} lessons completed",
            font=("Arial", 10, "bold"),
            bg=CARD_BG,
            fg="#444444"
        ).pack(anchor="w", padx=18)

        day_names = [
            "Day 1 • Introduction to Internet",
            "Day 2 • Web Browsers",
            "Day 3 • Search Engines",
            "Day 4 • Email",
            "Day 5 • Internet Safety"
        ]

        for i, day_name in enumerate(day_names, start=1):
            completed = i in completed_lessons

            row = tk.Frame(
                progress_card,
                bg="#F8F6FB",
                padx=10,
                pady=7
            )
            row.pack(
                fill="x",
                padx=18,
                pady=3
            )

            status = "✓ Completed" if completed else "🔒 Not Completed"
            status_color = GREEN if completed else "#888888"

            tk.Label(
                row,
                text=day_name,
                font=("Arial", 10, "bold"),
                bg="#F8F6FB",
                fg="#333333"
            ).pack(side="left")

            tk.Label(
                row,
                text=status,
                font=("Arial", 9, "bold"),
                bg="#F8F6FB",
                fg=status_color
            ).pack(side="right")

        # RIGHT: quiz progress + action
        right_column = tk.Frame(content, bg=BG)
        right_column.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        quiz_card = self.make_section_card(
            right_column,
            "❓ Your Quiz Progress"
        )
        quiz_card.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Label(
            quiz_card,
            text=f"Attempts: {attempts}",
            font=("Arial", 11, "bold"),
            bg=CARD_BG,
            fg="#333333"
        ).pack(anchor="w", padx=18, pady=2)

        tk.Label(
            quiz_card,
            text=(
                "Best Score: "
                + (
                    f"{float(best_percentage):.0f}%"
                    if best_percentage is not None
                    else "Not attempted"
                )
            ),
            font=("Arial", 11),
            bg=CARD_BG,
            fg="#555555"
        ).pack(anchor="w", padx=18, pady=2)

        tk.Label(
            quiz_card,
            text=(
                "Latest Score: "
                + (
                    f"{float(latest_percentage):.0f}%"
                    if latest_percentage is not None
                    else "Not attempted"
                )
            ),
            font=("Arial", 11),
            bg=CARD_BG,
            fg="#555555"
        ).pack(anchor="w", padx=18, pady=2)

        if latest_result:
            result_text = str(latest_result)
        elif attempts == 0:
            result_text = "Not Attempted"
        else:
            result_text = "Review your score"

        result_color = (
            GREEN
            if "pass" in result_text.lower()
            else "#B26A00"
        )

        tk.Label(
            quiz_card,
            text=f"Status: {result_text}",
            font=("Arial", 10, "bold"),
            bg=CARD_BG,
            fg=result_color
        ).pack(anchor="w", padx=18, pady=(2, 12))

        action_card = self.make_section_card(
            right_column,
            "🚀 Continue Learning"
        )
        action_card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            action_card,
            text=(
                "Read the lessons first, mark each day complete, "
                "then take the quiz."
            ),
            font=("Arial", 10),
            bg=CARD_BG,
            fg="#555555",
            wraplength=360,
            justify="left"
        ).pack(anchor="w", padx=18, pady=(0, 12))

        tk.Button(
            action_card,
            text="📚 Continue Course →",
            width=28,
            height=2,
            bg="#2196F3",
            fg="white",
            activebackground="#1565C0",
            activeforeground="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.open_course
        ).pack(padx=18, pady=5)

        tk.Button(
            action_card,
            text="❓ Take Quiz →",
            width=28,
            height=2,
            bg="#00A896",
            fg="white",
            activebackground="#00796B",
            activeforeground="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.open_quiz
        ).pack(padx=18, pady=5)

        tk.Button(
            action_card,
            text="🏆 Certificate",
            width=28,
            height=2,
            bg="#FF9800",
            fg="white",
            activebackground="#EF6C00",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.open_certificate
        ).pack(padx=18, pady=5)

        # ---------------- bottom ----------------
        bottom = tk.Frame(body, bg=BG)
        bottom.pack(fill="x", padx=28, pady=(0, 12))

        tk.Button(
            bottom,
            text="🔐 Admin Login",
            width=18,
            height=2,
            bg="#673AB7",
            fg="white",
            activebackground="#4527A0",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.open_admin
        ).pack(side="left")

        tk.Button(
            bottom,
            text="❌ Exit",
            width=14,
            height=2,
            bg="#E53935",
            fg="white",
            activebackground="#B71C1C",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.root.destroy
        ).pack(side="right")

    # ==================================================
    # PAGES
    # ==================================================

    def open_course(self):
        self.host.clear()

        CourseWindow(
            self.host,
            self.learner_id
        )

    def open_quiz(self):
        self.host.clear()

        QuizWindow(
            self.host,
            self.student_name,
            self.learner_id,
            on_pass=self.mark_quiz_passed,
            on_certificate=self.open_certificate
        )

    def mark_quiz_passed(self):
        self.quiz_passed_this_login = True

    def open_certificate(self):
        if not self.quiz_passed_this_login:
            messagebox.showwarning(
                "Certificate Page Locked",
                "Complete the quiz first to access the certificate page. "
                "You must score at least 70% to open it."
            )
            return

        self.host.clear()

        certificate.CertificateWindow(
            self.host,
            self.student_name,
            self.learner_id
        )

    def open_admin(self):
        self.host.clear()
        AdminLoginWindow(self.host, on_close=self.show_login)


# ======================================================
# START APPLICATION
# ======================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetBasicsApp(root)
    root.mainloop()
