import tkinter as tk
from tkinter import ttk


class StudentDashboard:

    def __init__(self, parent, username):
        self.parent = parent
        self.username = username

        self.frame = tk.Frame(
            parent,
            bg="#F5F7FA"
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.create_dashboard()

    def create_dashboard(self):

        # Header
        header = tk.Frame(
            self.frame,
            bg="#1F4E78",
            height=70
        )

        header.pack(
            fill="x"
        )

        title = tk.Label(
            header,
            text="🌐 Internet Basics",
            font=("Arial", 22, "bold"),
            bg="#1F4E78",
            fg="white"
        )

        title.pack(
            side="left",
            padx=25,
            pady=18
        )

        user_label = tk.Label(
            header,
            text=f"👤 {self.username}",
            font=("Arial", 12),
            bg="#1F4E78",
            fg="white"
        )

        user_label.pack(
            side="right",
            padx=25
        )

        # Welcome
        welcome = tk.Label(
            self.frame,
            text=f"👋 Welcome, {self.username}!",
            font=("Arial", 22, "bold"),
            bg="#F5F7FA",
            fg="#222222"
        )

        welcome.pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        subtitle = tk.Label(
            self.frame,
            text="Continue your digital learning journey.",
            font=("Arial", 12),
            bg="#F5F7FA",
            fg="#666666"
        )

        subtitle.pack(
            anchor="w",
            padx=30
        )

        # Statistics
        stats_frame = tk.Frame(
            self.frame,
            bg="#F5F7FA"
        )

        stats_frame.pack(
            fill="x",
            padx=30,
            pady=30
        )

        self.create_stat_card(
            stats_frame,
            "📚",
            "Lessons",
            "0 / 5"
        )

        self.create_stat_card(
            stats_frame,
            "⭐",
            "Best Score",
            "0%"
        )

        self.create_stat_card(
            stats_frame,
            "🏆",
            "Badges",
            "0"
        )

        # Progress
        progress_title = tk.Label(
            self.frame,
            text="📈 Your Learning Progress",
            font=("Arial", 16, "bold"),
            bg="#F5F7FA"
        )

        progress_title.pack(
            anchor="w",
            padx=30
        )

        progress = ttk.Progressbar(
            self.frame,
            orient="horizontal",
            length=600,
            mode="determinate"
        )

        progress["value"] = 0

        progress.pack(
            anchor="w",
            padx=30,
            pady=10
        )

        progress_label = tk.Label(
            self.frame,
            text="0% completed",
            font=("Arial", 11),
            bg="#F5F7FA",
            fg="#555555"
        )

        progress_label.pack(
            anchor="w",
            padx=30
        )

    def create_stat_card(
        self,
        parent,
        icon,
        title,
        value
    ):

        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            width=180,
            height=110
        )

        card.pack(
            side="left",
            padx=8,
            fill="both",
            expand=True
        )

        tk.Label(
            card,
            text=icon,
            font=("Arial", 25),
            bg="white"
        ).pack(
            pady=(12, 2)
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 10),
            bg="white",
            fg="#777777"
        ).pack()

        tk.Label(
            card,
            text=value,
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1F4E78"
        ).pack()