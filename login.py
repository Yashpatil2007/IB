import tkinter as tk
from tkinter import messagebox

from navigation import Page
import database


BG = "#F3E5F5"
PURPLE = "#6A1B9A"
PURPLE_DARK = "#4A148C"
TEAL = "#00A896"


class LoginWindow:
    """Learner login and registration page."""

    def __init__(self, parent, on_login, on_register=None):
        self.parent = parent
        self.on_login = on_login
        self.on_register = on_register or on_login

        self.window = Page(parent, bg=BG)
        self.show_login()

    def clear_card(self):
        for child in self.window.winfo_children():
            child.destroy()

    def make_card(self, title, subtitle):
        self.clear_card()

        card = tk.Frame(
            self.window,
            bg="white",
            highlightbackground="#D1C4E9",
            highlightthickness=1,
            padx=48,
            pady=30
        )
        card.place(relx=0.5, rely=0.48, anchor="center")

        tk.Label(
            card,
            text=title,
            font=("Arial", 24, "bold"),
            bg="white",
            fg=PURPLE
        ).pack(pady=(0, 6))

        tk.Label(
            card,
            text=subtitle,
            font=("Arial", 12),
            bg="white",
            fg="#555555",
            justify="center"
        ).pack(pady=(0, 20))

        return card

    def add_field(self, card, label):
        tk.Label(
            card,
            text=label,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333"
        ).pack(anchor="w")

        entry = tk.Entry(
            card,
            font=("Arial", 13),
            width=32,
            relief="solid"
        )
        entry.pack(pady=(4, 14), ipady=4)

        return entry

    # --------------------------------------------------
    # ADMIN LOGIN
    # --------------------------------------------------

    def open_admin_login(self):
        try:
            from admin import AdminLoginWindow

            self.window.destroy_silently()
            AdminLoginWindow(
                self.parent,
                on_close=self.return_to_login
            )

        except Exception as error:
            print("Could not open Admin Login:", error)
            messagebox.showerror(
                "Admin Login",
                f"Could not open the Admin Login page.\n\n{error}"
            )

    def return_to_login(self):
        LoginWindow(
            self.parent,
            self.on_login,
            self.on_register
        )

    def add_admin_button(self, card):
        tk.Frame(
            card,
            bg="#E0E0E0",
            height=1
        ).pack(fill="x", pady=(18, 12))

        tk.Label(
            card,
            text="OR",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#999999"
        ).pack(pady=(0, 8))

        button = tk.Button(
            card,
            text="🔐 Admin Login",
            font=("Arial", 11, "bold"),
            bg=PURPLE_DARK,
            fg="white",
            activebackground="#311B92",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=24,
            height=2,
            command=self.open_admin_login
        )
        button.pack()

        button.bind(
            "<Enter>",
            lambda event: button.configure(bg="#311B92")
        )
        button.bind(
            "<Leave>",
            lambda event: button.configure(bg=PURPLE_DARK)
        )

    # --------------------------------------------------
    # LEARNER LOGIN
    # --------------------------------------------------

    def show_login(self):
        card = self.make_card(
            "👤 Learner Login",
            "Welcome to Internet Basics! 🌐\n"
            "Sign in with your registered details."
        )

        self.name_entry = self.add_field(
            card,
            "👤 Student Name"
        )

        self.email_entry = self.add_field(
            card,
            "📧 Email ID"
        )

        tk.Button(
            card,
            text="🚀 Start Learning",
            font=("Arial", 14, "bold"),
            bg=TEAL,
            fg="white",
            activebackground="#00796B",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=22,
            height=2,
            command=self.login
        ).pack(pady=(2, 10))

        tk.Label(
            card,
            text="New learner? Create an account to register.",
            font=("Arial", 10),
            bg="white",
            fg="#666666"
        ).pack(pady=(4, 5))

        tk.Button(
            card,
            text="📝 Create New Account / Register",
            font=("Arial", 11, "bold"),
            bg="#7B4BB3",
            fg="white",
            activebackground="#6A3CA0",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.show_registration
        ).pack()

        self.add_admin_button(card)

        self.window.winfo_toplevel().bind(
            "<Return>",
            lambda event: self.login()
        )

        self.name_entry.focus_set()

    # --------------------------------------------------
    # LEARNER REGISTRATION
    # --------------------------------------------------

    def show_registration(self):
        card = self.make_card(
            "📝 Learner Registration",
            "Create your account to begin your learning journey."
        )

        self.reg_name = self.add_field(
            card,
            "👤 Full Name"
        )

        self.reg_email = self.add_field(
            card,
            "📧 Email ID"
        )

        tk.Button(
            card,
            text="✅ Register Account",
            font=("Arial", 14, "bold"),
            bg=TEAL,
            fg="white",
            activebackground="#00796B",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=22,
            height=2,
            command=self.register
        ).pack(pady=(4, 10))

        tk.Button(
            card,
            text="← Back to Login",
            font=("Arial", 11, "bold"),
            bg="#7B4BB3",
            fg="white",
            activebackground="#6A3CA0",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.show_login
        ).pack()

        self.add_admin_button(card)

        self.window.winfo_toplevel().bind(
            "<Return>",
            lambda event: self.register()
        )

        self.reg_name.focus_set()

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    def valid_details(self, name, email):
        if not name:
            messagebox.showwarning(
                "Missing Name",
                "Please enter your name."
            )
            return False

        if not email:
            messagebox.showwarning(
                "Missing Email",
                "Please enter your email ID."
            )
            return False

        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email ID."
            )
            return False

        return True

    # --------------------------------------------------
    # LOGIN
    # --------------------------------------------------

    def login(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip().lower()

        if not self.valid_details(name, email):
            return

        learner = database.get_learner(name, email)

        if not learner:
            messagebox.showerror(
                "Account Not Found",
                "No registered account matches these details. "
                "Please register first."
            )
            return

        self.window.destroy_silently()
        self.on_login(name, email)

    # --------------------------------------------------
    # REGISTRATION
    # --------------------------------------------------

    def register(self):
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip().lower()

        if not self.valid_details(name, email):
            return

        success, msg = database.register_learner(
            name,
            email
        )

        if not success:
            messagebox.showerror(
                "Registration",
                msg
            )
            return

        messagebox.showinfo(
            "Registration Successful",
            msg
        )

        self.window.destroy_silently()
        self.on_register(name, email)
