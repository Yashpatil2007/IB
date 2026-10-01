import os

import re

import io

import tempfile

import tkinter as tk

from tkinter import filedialog, messagebox

from datetime import datetime

from math import cos, sin, pi



from navigation import Page



try:

    from PIL import Image, ImageTk, ImageDraw, ImageFont

    import qrcode



    PIL_AVAILABLE = True

except Exception:

    PIL_AVAILABLE = False





# ==========================================================

# CERTIFICATE DESIGN

# ==========================================================



PAGE_BG = "#EFE5D2"

PAPER = "#FFFFFF"

GOLD = "#E3A51A"

GOLD_DARK = "#C98A08"

BLUE = "#24479B"

BLUE_DARK = "#18377D"

GREEN = "#66A84A"

RED = "#A92737"

BLACK = "#111111"

MUTED = "#6D6D6D"



INSTITUTE_NAME = "Internet Basics Learning System"

COURSE_NAME = "5-Day Internet Basics Course"

LEFT_SIGNATORY = "Course Instructor"

LEFT_TITLE = "Instructor"

RIGHT_SIGNATORY = "Training & Placement Cell"

RIGHT_TITLE = "Director of Training"





class CertificateWindow:



    def __init__(

        self,

        parent,

        student_name="Student",

        learner_id=None,

        score=None,

        percentage=None

    ):

        self.student_name = str(student_name or "Student")

        self.learner_id = learner_id

        self.score = score

        self.percentage = percentage



        self.window = Page(parent)

        self.window.title("Certificate of Appreciation")

        self.window.geometry("1180x790")

        self.window.minsize(1000, 700)

        self.window.configure(bg=PAGE_BG)



        self.issue_date = datetime.now().strftime("%d %B %Y")

        self.load_latest_quiz_result()



        self.certificate_id = self.make_certificate_id()



        self.certificate_image = None

        self.display_photo = None

        self.display_scale = 1.0

        self.display_x = 0

        self.display_y = 0



        self.create_ui()

        self.window.after(100, self.refresh_preview)



    # ==========================================================

    # DATABASE

    # ==========================================================



    def load_latest_quiz_result(self):



        if self.score is not None and self.percentage is not None:

            return



        try:

            import database

        except Exception:

            return



        try:

            connection = database.connect_database()

            cursor = connection.cursor()



            if self.learner_id is not None:

                cursor.execute(

                    """

                    SELECT score, total_questions, percentage

                    FROM quiz_attempts

                    WHERE learner_id = ?

                    ORDER BY id DESC

                    LIMIT 1

                    """,

                    (self.learner_id,)

                )

            else:

                cursor.execute(

                    """

                    SELECT qa.score, qa.total_questions, qa.percentage

                    FROM quiz_attempts AS qa

                    INNER JOIN learners AS l

                        ON l.id = qa.learner_id

                    WHERE l.name = ?

                    ORDER BY qa.id DESC

                    LIMIT 1

                    """,

                    (self.student_name,)

                )



            row = cursor.fetchone()

            connection.close()



            if row:

                if self.score is None:

                    self.score = row[0]



                if self.percentage is None:

                    self.percentage = row[2]



        except Exception as error:

            print("Could not load latest quiz result:", error)



    # ==========================================================

    # HELPERS

    # ==========================================================



    def make_certificate_id(self):

        clean_name = re.sub(

            r"[^A-Za-z0-9]",

            "",

            self.student_name

        ).upper()



        name_part = clean_name[:4] if clean_name else "STUD"



        learner_part = str(

            self.learner_id

            if self.learner_id is not None

            else "X"

        )



        learner_part = re.sub(

            r"[^A-Za-z0-9]",

            "",

            learner_part

        )[:6]



        return (

            f"IBC-{datetime.now().strftime('%Y%m%d')}-"

            f"{name_part}-{learner_part}"

        )



    def score_text(self):

        return (

            f"{self.score}/10"

            if self.score is not None

            else "Passed"

        )



    def percentage_text(self):

        if self.percentage is None:

            return "Passed"



        try:

            return f"{float(self.percentage):.0f}%"

        except Exception:

            return str(self.percentage)



    def get_qr_payload(self):

        return (

            "INTERNET BASICS LEARNING SYSTEM\n"

            "CERTIFICATE OF APPRECIATION\n"

            f"Certificate ID: {self.certificate_id}\n"

            f"Student: {self.student_name}\n"

            f"Course: {COURSE_NAME}\n"

            f"Score: {self.score_text()}\n"

            f"Result: PASSED ({self.percentage_text()})\n"

            f"Issue Date: {self.issue_date}"

        )



    # ==========================================================

    # FONTS

    # ==========================================================



    def font(self, paths, size):

        for path in paths:

            if os.path.exists(path):

                try:

                    return ImageFont.truetype(path, size)

                except Exception:

                    pass



        try:

            return ImageFont.truetype("DejaVuSans.ttf", size)

        except Exception:

            return ImageFont.load_default()



    def get_fonts(self):

        title = self.font(

            [

                r"C:\Windows\Fonts\georgiab.ttf",

                r"C:\Windows\Fonts\timesbd.ttf",

            ],

            48

        )



        institute = self.font(

            [

                r"C:\Windows\Fonts\segoeuib.ttf",

                r"C:\Windows\Fonts\arialbd.ttf",

                r"C:\Windows\Fonts\segoeui.ttf",

            ],

            29

        )



        name = self.font(

            [

                r"C:\Windows\Fonts\MTCORSVA.TTF",

                r"C:\Windows\Fonts\ITCEDSCR.TTF",

                r"C:\Windows\Fonts\BRUSHSCI.TTF",

                r"C:\Windows\Fonts\segoesc.ttf",

            ],

            68

        )



        body = self.font(

            [

                r"C:\Windows\Fonts\segoeui.ttf",

                r"C:\Windows\Fonts\arial.ttf",

            ],

            18

        )



        small = self.font(

            [

                r"C:\Windows\Fonts\segoeui.ttf",

                r"C:\Windows\Fonts\arial.ttf",

            ],

            14

        )



        signature = self.font(

            [

                r"C:\Windows\Fonts\segoesc.ttf",

                r"C:\Windows\Fonts\segoeui.ttf",

            ],

            20

        )



        return title, institute, name, body, small, signature



    # ==========================================================

    # DRAW HELPERS

    # ==========================================================



    def center_text(self, draw, xy, text, font, fill, anchor="mm"):

        draw.text(

            xy,

            text,

            font=font,

            fill=fill,

            anchor=anchor

        )



    def wrap_lines(self, text, width_chars=100):

        words = text.split()

        lines = []

        current = ""



        for word in words:

            test = word if not current else current + " " + word

            if len(test) <= width_chars:

                current = test

            else:

                if current:

                    lines.append(current)

                current = word



        if current:

            lines.append(current)



        return lines



    # ==========================================================

    # STAR MEDAL

    # ==========================================================



    def star_points(self, cx, cy, outer, inner, points=5):

        result = []



        for index in range(points * 2):

            angle = -pi / 2 + (pi * index / points)

            radius = outer if index % 2 == 0 else inner



            result.append(

                (

                    cx + cos(angle) * radius,

                    cy + sin(angle) * radius

                )

            )



        return result



    def draw_star(self, draw, cx, cy, outer, inner, fill, outline=None, width=1):

        points = self.star_points(

            cx,

            cy,

            outer,

            inner

        )



        draw.polygon(

            points,

            fill=fill

        )



        if outline:

            draw.line(

                points + [points[0]],

                fill=outline,

                width=width,

                joint="curve"

            )



    def draw_medal(self, draw):

        """

        Small decorative star badge on the LEFT side.

        It stays compact so it does not dominate the certificate.

        """



        cx, cy = 145, 118



        # Small blue ribbon rays

        for i in range(16):

            angle = (2 * pi * i) / 16



            x1 = cx + cos(angle) * 24

            y1 = cy + sin(angle) * 24

            x2 = cx + cos(angle) * 42

            y2 = cy + sin(angle) * 42



            draw.line(

                (x1, y1, x2, y2),

                fill=BLUE,

                width=7

            )



        # Small gold medal

        draw.ellipse(

            (115, 88, 175, 148),

            fill="#F9B91E",

            outline=GOLD_DARK,

            width=2

        )



        draw.ellipse(

            (121, 94, 169, 142),

            fill="#FFD94D",

            outline="#FFF1A6",

            width=2

        )



        self.draw_star(

            draw,

            145,

            118,

            22,

            9,

            "#FFF4B0",

            outline="#D4910C",

            width=2

        )



        # Small decorative stars around the badge

        for sx, sy, outer in [

            (91, 84, 8),

            (84, 120, 6),

            (199, 90, 8),

            (202, 124, 6),

        ]:

            self.draw_star(

                draw,

                sx,

                sy,

                outer,

                outer * 0.42,

                "#F8B918",

                outline="#D4910C",

                width=1

            )



    # ==========================================================

    # CERTIFIED SEAL

    # ==========================================================



    def draw_certified_seal(self, draw):

        cx, cy = 740, 735



        # Compact green certified seal

        draw.ellipse(

            (680, 675, 800, 795),

            fill="#F7FFF1",

            outline=GREEN,

            width=5

        )



        draw.ellipse(

            (692, 687, 788, 783),

            outline=GREEN,

            width=2

        )



        # Check mark

        draw.line(

            (716, 737, 737, 758, 770, 716),

            fill=GREEN,

            width=10,

            joint="curve"

        )



        seal_font = self.font(

            [

                r"C:\Windows\Fonts\arialbd.ttf",

            ],

            10

        )



        self.center_text(

            draw,

            (740, 704),

            "CERTIFIED",

            seal_font,

            GREEN

        )



        self.center_text(

            draw,

            (740, 775),

            "CERTIFIED",

            seal_font,

            GREEN

        )



        draw.text(

            (704, 731),

            "★",

            font=seal_font,

            fill=GREEN

        )



        draw.text(

            (765, 731),

            "★",

            font=seal_font,

            fill=GREEN

        )



    # ==========================================================

    # CERTIFICATE IMAGE

    # ==========================================================



    def render_certificate(self):

        if not PIL_AVAILABLE:

            return None



        width = 1400

        height = 900



        image = Image.new(

            "RGB",

            (width, height),

            PAPER

        )



        draw = ImageDraw.Draw(image)



        (

            title_font,

            institute_font,

            name_font,

            body_font,

            small_font,

            signature_font

        ) = self.get_fonts()



        # ------------------------------------------------------

        # BACKGROUND / BORDER

        # ------------------------------------------------------



        draw.rectangle(

            (0, 0, width - 1, height - 1),

            fill=PAPER

        )



        # Outer gold border

        draw.rectangle(

            (28, 28, 1372, 872),

            outline=GOLD,

            width=4

        )



        # Inner gold border

        draw.rectangle(

            (42, 42, 1358, 858),

            outline=GOLD,

            width=2

        )



        # Ornamental corner arcs

        corner = 78



        for x0, y0, x1, y1, start in [

            (28, 28, 110, 110, 0),

            (1290, 28, 1372, 110, 90),

            (1290, 790, 1372, 872, 180),

            (28, 790, 110, 872, 270),

        ]:

            draw.arc(

                (x0, y0, x1, y1),

                start=start,

                end=start + 90,

                fill=GOLD,

                width=4

            )



        # ------------------------------------------------------

        # TOP MEDAL + STARS

        # ------------------------------------------------------



        self.draw_medal(draw)



        self.center_text(

            draw,

            (705, 118),

            INSTITUTE_NAME,

            institute_font,

            BLACK

        )



        draw.line(

            (330, 155, 1080, 155),

            fill=GOLD,

            width=2

        )



        self.draw_star(

            draw,

            705,

            155,

            7,

            3,

            GOLD

        )



        # ------------------------------------------------------

        # TITLE

        # ------------------------------------------------------



        self.center_text(

            draw,

            (705, 235),

            "CERTIFICATE OF APPRECIATION",

            title_font,

            BLACK

        )



        self.center_text(

            draw,

            (705, 285),

            "This Certificate is Proudly Awarded to",

            body_font,

            BLACK

        )



        # ------------------------------------------------------

        # NAME

        # ------------------------------------------------------



        self.center_text(

            draw,

            (705, 355),

            self.student_name,

            name_font,

            BLACK

        )



        draw.line(

            (500, 430, 910, 430),

            fill=GOLD,

            width=2

        )



        # ------------------------------------------------------

        # COURSE / ACHIEVEMENT

        # ------------------------------------------------------



        paragraph = (

            f"For successfully completing the {COURSE_NAME}. "

            "Your commitment to learning, active participation, "

            "and dedication to mastering essential digital skills "

            "have demonstrated true professionalism and a passion "

            "for growth. Through perseverance and determination, "

            "you have achieved an outstanding milestone in your "

            "educational journey."

        )



        lines = self.wrap_lines(

            paragraph,

            112

        )



        y = 465



        for line in lines[:4]:

            self.center_text(

                draw,

                (705, y),

                line,

                small_font,

                BLACK

            )

            y += 22



        # ------------------------------------------------------

        # COURSE + RESULT INFO

        # ------------------------------------------------------



        info_font = self.font(

            [

                r"C:\Windows\Fonts\arialbd.ttf",

                r"C:\Windows\Fonts\segoeuib.ttf",

            ],

            15

        )



        info_text = (

            f"Quiz Score: {self.score_text()}    •    "

            f"Result: PASSED ({self.percentage_text()})    •    "

            f"Date: {self.issue_date}"

        )



        self.center_text(

            draw,

            (705, 595),

            info_text,

            info_font,

            MUTED

        )



        # ------------------------------------------------------

        # SIGNATURES

        # ------------------------------------------------------



        draw.line(

            (150, 760, 395, 760),

            fill="#777777",

            width=1

        )



        self.center_text(

            draw,

            (272, 735),

            LEFT_SIGNATORY,

            signature_font,

            BLACK

        )



        self.center_text(

            draw,

            (272, 783),

            LEFT_TITLE,

            small_font,

            BLACK

        )



        draw.line(

            (875, 760, 1120, 760),

            fill="#777777",

            width=1

        )



        self.center_text(

            draw,

            (998, 735),

            RIGHT_SIGNATORY,

            signature_font,

            BLACK

        )



        self.center_text(

            draw,

            (998, 783),

            RIGHT_TITLE,

            small_font,

            BLACK

        )



        # ------------------------------------------------------

        # QR CODE

        # ------------------------------------------------------



        qr = qrcode.QRCode(

            version=None,

            error_correction=qrcode.constants.ERROR_CORRECT_M,

            box_size=4,

            border=1

        )



        qr.add_data(

            self.get_qr_payload()

        )



        qr.make(

            fit=True

        )



        qr_image = qr.make_image(

            fill_color="black",

            back_color="white"

        ).convert("RGB")



        qr_image = qr_image.resize(

            (120, 120),

            Image.Resampling.NEAREST

        )



        image.paste(

            qr_image,

            (520, 680)

        )



        qr_id_font = self.font(

            [

                r"C:\Windows\Fonts\arial.ttf"

            ],

            8

        )



        self.center_text(

            draw,

            (580, 820),

            self.certificate_id,

            qr_id_font,

            MUTED

        )



        # ------------------------------------------------------

        # GREEN CERTIFIED SEAL

        # ------------------------------------------------------



        self.draw_certified_seal(

            draw

        )



        return image



    # ==========================================================

    # UI

    # ==========================================================



    def create_ui(self):



        header = tk.Frame(

            self.window,

            bg="#542C85",

            height=62

        )



        header.pack(

            fill="x"

        )



        header.pack_propagate(False)



        tk.Label(

            header,

            text="🏆 Certificate of Appreciation",

            font=("Arial", 20, "bold"),

            bg="#542C85",

            fg="white"

        ).pack(

            side="left",

            padx=22

        )



        tk.Label(

            header,

            text="Interactive Achievement Certificate",

            font=("Arial", 9, "bold"),

            bg="#542C85",

            fg="#EBDDFA"

        ).pack(

            side="right",

            padx=22

        )



        preview = tk.Frame(

            self.window,

            bg=PAGE_BG

        )



        preview.pack(

            fill="both",

            expand=True,

            padx=12,

            pady=(12, 8)

        )



        self.canvas = tk.Canvas(

            preview,

            bg=PAGE_BG,

            highlightthickness=0

        )



        self.canvas.pack(

            fill="both",

            expand=True

        )



        self.canvas.bind(

            "<Configure>",

            lambda event: self.refresh_preview()

        )



        self.canvas.bind(

            "<Button-1>",

            self.handle_certificate_click

        )



        self.canvas.bind(

            "<Motion>",

            self.handle_certificate_hover

        )



        actions = tk.Frame(

            self.window,

            bg=PAGE_BG,

            height=55

        )



        actions.pack(

            fill="x",

            padx=12,

            pady=(0, 10)

        )



        actions.pack_propagate(False)



        self.make_button(

            actions,

            "🔍 Verify Certificate",

            "#6A4BB2",

            "#543792",

            self.verify_certificate

        ).pack(

            side="left",

            padx=5

        )



        self.make_button(

            actions,

            "💾 Save PNG",

            "#00897B",

            "#00695C",

            self.save_certificate

        ).pack(

            side="left",

            padx=5

        )



        self.make_button(

            actions,

            "🖨 Print / PDF",

            "#1565C0",

            "#0D47A1",

            self.print_certificate

        ).pack(

            side="left",

            padx=5

        )



        self.make_button(

            actions,

            "✕ Close",

            "#757575",

            "#5E5E5E",

            self.window.destroy

        ).pack(

            side="right",

            padx=5

        )



    def make_button(

        self,

        parent,

        text,

        color,

        hover,

        command

    ):



        button = tk.Button(

            parent,

            text=text,

            font=("Arial", 10, "bold"),

            bg=color,

            fg="white",

            activebackground=hover,

            activeforeground="white",

            relief="flat",

            cursor="hand2",

            padx=14,

            pady=7,

            command=command

        )



        button.bind(

            "<Enter>",

            lambda event: button.configure(

                bg=hover

            )

        )



        button.bind(

            "<Leave>",

            lambda event: button.configure(

                bg=color

            )

        )



        return button



    # ==========================================================

    # PREVIEW

    # ==========================================================



    def refresh_preview(self):



        if not PIL_AVAILABLE:

            self.canvas.delete("all")



            self.canvas.create_text(

                500,

                300,

                text=(

                    "Certificate preview requires Pillow and qrcode.\n\n"

                    "Run:\n"

                    "pip install pillow qrcode"

                ),

                font=("Arial", 16, "bold"),

                fill=RED

            )



            return



        self.certificate_image = self.render_certificate()



        if self.certificate_image is None:

            return



        canvas_w = max(

            self.canvas.winfo_width(),

            700

        )



        canvas_h = max(

            self.canvas.winfo_height(),

            500

        )



        img_w, img_h = self.certificate_image.size



        scale = min(

            (canvas_w - 10) / img_w,

            (canvas_h - 10) / img_h

        )



        scale = min(

            scale,

            1.0

        )



        display_w = max(

            1,

            int(img_w * scale)

        )



        display_h = max(

            1,

            int(img_h * scale)

        )



        display_image = self.certificate_image.resize(

            (display_w, display_h),

            Image.Resampling.LANCZOS

        )



        self.display_photo = ImageTk.PhotoImage(

            display_image

        )



        self.display_scale = scale



        self.display_x = (

            canvas_w - display_w

        ) / 2



        self.display_y = (

            canvas_h - display_h

        ) / 2



        self.canvas.delete(

            "all"

        )



        self.canvas.create_image(

            self.display_x,

            self.display_y,

            image=self.display_photo,

            anchor="nw"

        )



    # ==========================================================

    # INTERACTIVE QR

    # ==========================================================



    def original_xy(

        self,

        event

    ):

        if self.display_scale <= 0:

            return 0, 0



        return (

            (event.x - self.display_x) / self.display_scale,

            (event.y - self.display_y) / self.display_scale

        )



    def qr_hover(

        self,

        x,

        y

    ):

        return (

            505 <= x <= 655

            and 655 <= y <= 820

        )



    def handle_certificate_hover(

        self,

        event

    ):

        try:

            x, y = self.original_xy(event)



            self.canvas.configure(

                cursor="hand2"

                if self.qr_hover(x, y)

                else ""

            )



        except Exception:

            pass



    def handle_certificate_click(

        self,

        event

    ):

        try:

            x, y = self.original_xy(event)



            if self.qr_hover(x, y):

                self.verify_certificate()



        except Exception:

            pass



    # ==========================================================

    # VERIFY

    # ==========================================================



    def verify_certificate(self):



        popup = tk.Toplevel(

            self.window

        )



        popup.title(

            "Certificate Verification"

        )



        popup.geometry(

            "520x460"

        )



        popup.configure(

            bg=PAGE_BG

        )



        popup.transient(

            self.window

        )



        popup.grab_set()



        tk.Label(

            popup,

            text="✓ Certificate Verified",

            font=("Arial", 23, "bold"),

            bg=PAGE_BG,

            fg=GREEN

        ).pack(

            pady=(28, 8)

        )



        card = tk.Frame(

            popup,

            bg="white",

            highlightbackground=GOLD,

            highlightthickness=2

        )



        card.pack(

            fill="x",

            padx=28

        )



        rows = [

            ("Student", self.student_name),

            ("Course", COURSE_NAME),

            ("Score", self.score_text()),

            ("Result", f"PASSED • {self.percentage_text()}"),

            ("Date", self.issue_date),

            ("Certificate ID", self.certificate_id)

        ]



        for label, value in rows:



            row = tk.Frame(

                card,

                bg="white"

            )



            row.pack(

                fill="x",

                padx=15,

                pady=5

            )



            tk.Label(

                row,

                text=label,

                width=16,

                anchor="w",

                font=("Arial", 9, "bold"),

                bg="white",

                fg=MUTED

            ).pack(

                side="left"

            )



            tk.Label(

                row,

                text=value,

                anchor="w",

                font=("Arial", 9, "bold"),

                bg="white",

                fg=BLACK,

                wraplength=290

            ).pack(

                side="left",

                fill="x",

                expand=True

            )



        tk.Label(

            popup,

            text="The QR code contains the same verification details.",

            font=("Arial", 9),

            bg=PAGE_BG,

            fg=MUTED

        ).pack(

            pady=14

        )



        self.make_button(

            popup,

            "Close",

            "#542C85",

            "#3D1F63",

            popup.destroy

        ).pack(

            pady=(0, 15)

        )



    # ==========================================================

    # SAVE

    # ==========================================================



    def save_certificate(self):



        if self.certificate_image is None:

            return



        safe_name = re.sub(

            r"[^A-Za-z0-9_-]+",

            "_",

            self.student_name

        ).strip("_")



        path = filedialog.asksaveasfilename(

            parent=self.window,

            title="Save Certificate",

            defaultextension=".png",

            initialfile=(

                f"Internet_Basics_Certificate_"

                f"{safe_name or 'Student'}.png"

            ),

            filetypes=[

                ("PNG Image", "*.png"),

                ("All Files", "*.*")

            ]

        )



        if not path:

            return



        self.certificate_image.save(

            path,

            "PNG"

        )



        messagebox.showinfo(

            "Certificate Saved",

            "Your achievement certificate has been saved successfully."

        )



    # ==========================================================

    # PRINT / PDF

    # ==========================================================



    def print_certificate(self):
        """Create and open a real A4 landscape PDF of the certificate."""
        if self.certificate_image is None:
            messagebox.showwarning(
                "Certificate",
                "Certificate is not ready yet."
            )
            return

        safe_name = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            self.student_name
        ).strip("_")

        pdf_path = filedialog.asksaveasfilename(
            parent=self.window,
            title="Save Certificate as PDF",
            defaultextension=".pdf",
            initialfile=(
                f"Internet_Basics_Certificate_"
                f"{safe_name or 'Student'}.pdf"
            ),
            filetypes=[
                ("PDF Document", "*.pdf"),
                ("All Files", "*.*")
            ]
        )

        if not pdf_path:
            return

        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.utils import ImageReader

            page_width, page_height = landscape(A4)
            pdf = canvas.Canvas(
                pdf_path,
                pagesize=(page_width, page_height)
            )

            image_width, image_height = self.certificate_image.size

            # Fit the complete certificate onto one A4 landscape page.
            scale = min(
                page_width / image_width,
                page_height / image_height
            )

            draw_width = image_width * scale
            draw_height = image_height * scale
            x = (page_width - draw_width) / 2
            y = (page_height - draw_height) / 2

            image_buffer = io.BytesIO()
            self.certificate_image.save(
                image_buffer,
                format="PNG"
            )
            image_buffer.seek(0)

            pdf.drawImage(
                ImageReader(image_buffer),
                x,
                y,
                width=draw_width,
                height=draw_height,
                preserveAspectRatio=True,
                mask="auto"
            )

            pdf.showPage()
            pdf.save()
            image_buffer.close()

            # Open the actual PDF instead of opening an HTML page in Chrome.
            os.startfile(os.path.abspath(pdf_path))

        except ImportError:
            messagebox.showerror(
                "PDF Support Missing",
                "ReportLab is required to create PDF certificates.\n\n"
                "Please install it using:\n\n"
                "pip install reportlab"
            )

        except Exception as error:
            messagebox.showerror(
                "Print / PDF Error",
                f"Could not create the PDF:\n\n{error}"
            )



if __name__ == "__main__":



    root = tk.Tk()

    root.geometry("1250x900")

    CertificateWindow(

        root,

        "Shaikh Naz"

    )

    root.mainloop()
