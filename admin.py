import tkinter as tk
from tkinter import ttk, messagebox

from navigation import Page
import database


# ----------------------------------------------------------
# ADMIN CREDENTIALS
# ----------------------------------------------------------

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ----------------------------------------------------------
# COLORS
# ----------------------------------------------------------

PURPLE = "#542C85"
PURPLE_DARK = "#3D1F63"
LIGHT_PURPLE = "#F5F0FF"
CARD = "#FFFFFF"
TEXT = "#2E2E2E"
MUTED = "#777777"
GREEN = "#2E7D32"
RED = "#C62828"
TEAL = "#00897B"
BLUE = "#1565C0"


# ==========================================================
# ADMIN LOGIN
# ==========================================================

class AdminLoginWindow:

    def __init__(self, parent, on_close=None):

        self.parent = parent
        self.on_close = on_close

        self.window = Page(
            parent,
            bg=LIGHT_PURPLE
        )

        self.window.title(
            "Admin Login"
        )

        self.window.configure(
            bg=LIGHT_PURPLE
        )

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        # Header
        header = tk.Frame(
            self.window,
            bg=PURPLE,
            height=105
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🔐",
            font=("Arial", 30),
            bg=PURPLE,
            fg="white"
        ).pack(
            pady=(12, 0)
        )

        tk.Label(
            header,
            text="Admin Login",
            font=("Arial", 24, "bold"),
            bg=PURPLE,
            fg="white"
        ).pack()

        # Main area
        center = tk.Frame(
            self.window,
            bg=LIGHT_PURPLE
        )

        center.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            center,
            bg=CARD,
            highlightbackground="#D8C9EC",
            highlightthickness=1,
            padx=45,
            pady=30
        )

        card.place(
            relx=0.5,
            rely=0.48,
            anchor="center"
        )

        tk.Label(
            card,
            text="Secure access to the administration dashboard",
            font=("Arial", 11),
            bg=CARD,
            fg=MUTED
        ).pack(
            pady=(0, 22)
        )

        # Username
        tk.Label(
            card,
            text="👤 Admin Username",
            font=("Arial", 11, "bold"),
            bg=CARD,
            fg=PURPLE_DARK
        ).pack(anchor="w")

        self.username_entry = tk.Entry(
            card,
            font=("Arial", 13),
            width=34,
            relief="solid",
            bd=1
        )

        self.username_entry.pack(
            fill="x",
            pady=(6, 16),
            ipady=6
        )

        # Password
        tk.Label(
            card,
            text="🔑 Admin Password",
            font=("Arial", 11, "bold"),
            bg=CARD,
            fg=PURPLE_DARK
        ).pack(anchor="w")

        password_frame = tk.Frame(
            card,
            bg=CARD
        )

        password_frame.pack(
            fill="x",
            pady=(6, 20)
        )

        self.password_entry = tk.Entry(
            password_frame,
            font=("Arial", 13),
            relief="solid",
            bd=1,
            show="•"
        )

        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=6
        )

        self.show_password = False

        tk.Button(
            password_frame,
            text="👁",
            font=("Arial", 10),
            bg=CARD,
            fg=PURPLE,
            relief="flat",
            cursor="hand2",
            command=self.toggle_password
        ).pack(
            side="right",
            padx=(5, 0)
        )

        # Login
        login_button = tk.Button(
            card,
            text="🚪 Login to Dashboard",
            font=("Arial", 13, "bold"),
            bg=PURPLE,
            fg="white",
            activebackground=PURPLE_DARK,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            height=2,
            command=self.login
        )

        login_button.pack(
            fill="x"
        )

        login_button.bind(
            "<Enter>",
            lambda event: login_button.configure(
                bg=PURPLE_DARK
            )
        )

        login_button.bind(
            "<Leave>",
            lambda event: login_button.configure(
                bg=PURPLE
            )
        )

        # Close
        tk.Button(
            card,
            text="✕ Close",
            font=("Arial", 11, "bold"),
            bg="#EEEEEE",
            fg="#444444",
            activebackground="#DDDDDD",
            relief="flat",
            cursor="hand2",
            command=self.close
        ).pack(
            fill="x",
            pady=(12, 0)
        )

        # Footer
        tk.Label(
            card,
            text="🛡 Authorized administrators only",
            font=("Arial", 9),
            bg=CARD,
            fg=MUTED
        ).pack(
            pady=(18, 0)
        )

        self.window.winfo_toplevel().bind(
            "<Return>",
            lambda event: self.login()
        )

        self.username_entry.focus_set()

    # ======================================================
    # ACTIONS
    # ======================================================

    def toggle_password(self):

        self.show_password = not self.show_password

        self.password_entry.configure(
            show="" if self.show_password else "•"
        )

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:

            messagebox.showwarning(
                "Missing Details",
                "Please enter both admin username and password."
            )

            return

        if (
            username != ADMIN_USERNAME
            or password != ADMIN_PASSWORD
        ):

            messagebox.showerror(
                "Login Failed",
                "Invalid administrator username or password."
            )

            return

        self.window.destroy_silently()

        AdminDashboard(
            self.parent,
            on_logout=self.on_close
        )

    def close(self):

        self.window.destroy_silently()
        if self.on_close:
            self.on_close()


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

class AdminDashboard:

    def __init__(self, parent, on_logout=None):

        self.parent = parent
        self.on_logout = on_logout

        self.window = Page(
            parent,
            bg=LIGHT_PURPLE
        )

        self.window.title(
            "Admin Dashboard"
        )

        self.build_ui()

        self.refresh_data()

    # ======================================================
    # DASHBOARD UI
    # ======================================================

    def build_ui(self):

        header = tk.Frame(
            self.window,
            bg=PURPLE,
            height=68
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🛡 Admin Dashboard",
            font=("Arial", 21, "bold"),
            bg=PURPLE,
            fg="white"
        ).pack(
            side="left",
            padx=24
        )

        tk.Button(
            header,
            text="🚪 Logout",
            font=("Arial", 10, "bold"),
            bg="#7B4BB3",
            fg="white",
            activebackground="#6A3CA0",
            relief="flat",
            cursor="hand2",
            command=self.close
        ).pack(
            side="right",
            padx=20
        )

        # --------------------------------------------------
        # STATISTICS
        # --------------------------------------------------

        stats = tk.Frame(
            self.window,
            bg=LIGHT_PURPLE
        )

        stats.pack(
            fill="x",
            padx=20,
            pady=18
        )

        self.total_value = self.stat_card(
            stats,
            "👥 Total Learners",
            0,
            PURPLE
        )

        self.attempt_value = self.stat_card(
            stats,
            "📝 Quiz Attempts",
            0,
            TEAL
        )

        self.pass_value = self.stat_card(
            stats,
            "✅ Passed",
            0,
            GREEN
        )

        self.average_value = self.stat_card(
            stats,
            "📊 Average Score",
            "0%",
            BLUE
        )

        # --------------------------------------------------
        # LEARNER SECTION
        # --------------------------------------------------

        content = tk.Frame(
            self.window,
            bg=LIGHT_PURPLE
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        top = tk.Frame(
            content,
            bg=LIGHT_PURPLE
        )

        top.pack(
            fill="x",
            pady=(0, 8)
        )

        tk.Label(
            top,
            text="Registered Learners",
            font=("Arial", 17, "bold"),
            bg=LIGHT_PURPLE,
            fg=PURPLE_DARK
        ).pack(
            side="left"
        )

        tk.Button(
            top,
            text="🔄 Refresh",
            font=("Arial", 10, "bold"),
            bg=TEAL,
            fg="white",
            activebackground="#00695C",
            relief="flat",
            cursor="hand2",
            command=self.refresh_data
        ).pack(
            side="right"
        )

        # --------------------------------------------------
        # TABLE
        # --------------------------------------------------

        table_frame = tk.Frame(
            content,
            bg="white",
            highlightbackground="#D8C9EC",
            highlightthickness=1
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "id",
            "name",
            "email",
            "started"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "name": "Student Name",
            "email": "Email",
            "started": "Course Started"
        }

        widths = {
            "id": 70,
            "name": 230,
            "email": 330,
            "started": 180
        }

        for column in columns:

            self.table.heading(
                column,
                text=headings[column]
            )

            self.table.column(
                column,
                width=widths[column],
                anchor="w"
            )

        scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scroll.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        scroll.pack(
            side="right",
            fill="y",
            pady=8
        )

    # ======================================================
    # STAT CARD
    # ======================================================

    def stat_card(
        self,
        parent,
        title,
        value,
        accent
    ):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#D8C9EC",
            highlightthickness=1,
            width=230,
            height=90
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            bg="white",
            fg=MUTED
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 0)
        )

        value_label = tk.Label(
            card,
            text=str(value),
            font=("Arial", 24, "bold"),
            bg="white",
            fg=accent
        )

        value_label.pack(
            anchor="w",
            padx=15
        )

        return value_label

    # ======================================================
    # DATA
    # ======================================================

    def refresh_data(self):

        try:

            learners = database.get_all_learners()

            # Clear existing table
            for item in self.table.get_children():

                self.table.delete(item)

            # Insert learners
            for learner in learners:

                learner_id = learner[0]
                name = learner[1]
                email = learner[2]

                started = (
                    learner[3]
                    if len(learner) > 3
                    else ""
                )

                self.table.insert(
                    "",
                    "end",
                    values=(
                        learner_id,
                        name,
                        email,
                        started
                    )
                )

            # Total learners
            self.total_value.configure(
                text=str(len(learners))
            )

        except Exception as error:

            print(
                "Learner data error:",
                error
            )

            self.total_value.configure(
                text="0"
            )

        # Load quiz statistics
        self.load_quiz_stats()

    # ======================================================
    # OVERALL QUIZ STATISTICS
    # ======================================================

    def load_quiz_stats(self):

        try:

            # IMPORTANT:
            # Admin dashboard needs statistics for ALL learners.
            # Therefore we use get_overall_quiz_statistics()
            # instead of get_quiz_statistics(learner_id).

            stats = database.get_overall_quiz_statistics()

            attempts = 0
            passed = 0
            average = 0

            if isinstance(stats, dict):

                attempts = stats.get(
                    "attempts",
                    0
                )

                passed = stats.get(
                    "passed",
                    0
                )

                average = stats.get(
                    "average_percentage",
                    0
                )

            # Quiz Attempts
            self.attempt_value.configure(
                text=str(attempts)
            )

            # Passed
            self.pass_value.configure(
                text=str(passed)
            )

            # Average Score
            self.average_value.configure(
                text=f"{float(average):.0f}%"
            )

        except Exception as error:

            print(
                "Quiz statistics error:",
                error
            )

            self.attempt_value.configure(
                text="0"
            )

            self.pass_value.configure(
                text="0"
            )

            self.average_value.configure(
                text="0% "
            )

    # ======================================================
    # CLOSE
    # ======================================================

    def close(self):

        self.window.destroy_silently()
        if self.on_logout:
            self.on_logout()


# ==========================================================
# STANDALONE TEST
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "Internet Basics Learning System - Admin"
    )

    root.geometry(
        "1180x760"
    )

    AdminLoginWindow(root)

    root.mainloop()