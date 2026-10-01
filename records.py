import tkinter as tk
from navigation import Page
from tkinter import ttk, messagebox
import database


class RecordsWindow:

    def __init__(self, parent):

        self.window = Page(parent)

        self.window.title("Learner Records")
        self.window.geometry("1000x600")
        self.window.configure(bg="#F5F0FF")

        # ==================================================
        # HEADER
        # ==================================================

        header = tk.Frame(
            self.window,
            bg="#542C85",
            height=80
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="📊 Learner Records Dashboard",
            font=("Arial", 23, "bold"),
            bg="#542C85",
            fg="white"
        )

        title.pack(
            pady=20
        )

        # ==================================================
        # INFORMATION
        # ==================================================

        info_frame = tk.Frame(
            self.window,
            bg="#F5F0FF"
        )

        info_frame.pack(
            pady=20
        )

        self.total_label = tk.Label(
            info_frame,
            text="👥 Total Learners: 0",
            font=("Arial", 16, "bold"),
            bg="#2196F3",
            fg="white",
            padx=25,
            pady=10
        )

        self.total_label.pack(
            side="left",
            padx=10
        )

        self.attempt_label = tk.Label(
            info_frame,
            text="📝 Total Quiz Attempts: 0",
            font=("Arial", 16, "bold"),
            bg="#00A896",
            fg="white",
            padx=25,
            pady=10
        )

        self.attempt_label.pack(
            side="left",
            padx=10
        )

        # ==================================================
        # TABLE FRAME
        # ==================================================

        table_frame = tk.Frame(
            self.window,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        # ==================================================
        # TABLE
        # ==================================================

        columns = (
            "ID",
            "Name",
            "Email",
            "Attempts",
            "Best Score",
            "Percentage"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        # Column headings

        self.table.heading(
            "ID",
            text="ID"
        )

        self.table.heading(
            "Name",
            text="Student Name"
        )

        self.table.heading(
            "Email",
            text="Email ID"
        )

        self.table.heading(
            "Attempts",
            text="Quiz Attempts"
        )

        self.table.heading(
            "Best Score",
            text="Best Score"
        )

        self.table.heading(
            "Percentage",
            text="Best Percentage"
        )

        # Column widths

        self.table.column(
            "ID",
            width=50,
            anchor="center"
        )

        self.table.column(
            "Name",
            width=180
        )

        self.table.column(
            "Email",
            width=280
        )

        self.table.column(
            "Attempts",
            width=120,
            anchor="center"
        )

        self.table.column(
            "Best Score",
            width=120,
            anchor="center"
        )

        self.table.column(
            "Percentage",
            width=140,
            anchor="center"
        )

        # Scrollbar

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ==================================================
        # BUTTONS
        # ==================================================

        button_frame = tk.Frame(
            self.window,
            bg="#F5F0FF"
        )

        button_frame.pack(
            pady=15
        )

        refresh_button = tk.Button(
            button_frame,
            text="🔄 Refresh Records",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            activebackground="#1565C0",
            width=20,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.load_records
        )

        refresh_button.pack(
            side="left",
            padx=10
        )

        close_button = tk.Button(
            button_frame,
            text="❌ Close",
            font=("Arial", 12, "bold"),
            bg="#E53935",
            fg="white",
            activebackground="#B71C1C",
            width=15,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.window.destroy
        )

        close_button.pack(
            side="left",
            padx=10
        )

        # Load records

        self.load_records()

    # ==================================================
    # LOAD RECORDS
    # ==================================================

    def load_records(self):

        # Clear existing rows

        for row in self.table.get_children():

            self.table.delete(row)

        # Get learners

        learners = database.get_all_learners()

        total_learners = len(learners)

        total_attempts = 0

        for learner in learners:

            learner_id = learner[0]
            name = learner[1]
            email = learner[2]
            attempts = learner[3]

            best_percentage = learner[4]
            best_score = learner[5]

            if attempts is None:
                attempts = 0

            total_attempts += attempts

            if best_percentage is None:

                percentage_text = "No Quiz"

            else:

                percentage_text = f"{best_percentage:.0f}%"

            if best_score is None:

                score_text = "-"

            else:

                score_text = f"{int(best_score)}/10"

            self.table.insert(
                "",
                "end",
                values=(
                    learner_id,
                    name,
                    email,
                    attempts,
                    score_text,
                    percentage_text
                )
            )

        # Update statistics

        self.total_label.config(
            text=f"👥 Total Learners: {total_learners}"
        )

        self.attempt_label.config(
            text=f"📝 Total Quiz Attempts: {total_attempts}"
        )