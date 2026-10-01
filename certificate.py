"""Certificate rendering and Streamlit download controls."""

from datetime import datetime
from io import BytesIO
import re

import qrcode
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

import database


def _font(size, bold=False):
    candidates = (
        ("arialbd.ttf", "DejaVuSans-Bold.ttf")
        if bold
        else ("arial.ttf", "DejaVuSans.ttf")
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def create_certificate_image(user, percentage):
    width, height = 1600, 1100
    image = Image.new("RGB", (width, height), "#fbfaf6")
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        (38, 38, width - 38, height - 38),
        radius=24,
        outline="#173b4f",
        width=8,
    )
    draw.rounded_rectangle(
        (62, 62, width - 62, height - 62),
        radius=18,
        outline="#c39b4a",
        width=3,
    )

    draw.text((width // 2, 155), "INTERNET BASICS LEARNING SYSTEM", font=_font(32, True), fill="#173b4f", anchor="mm")
    draw.line((310, 205, width - 310, 205), fill="#c39b4a", width=3)
    draw.text((width // 2, 315), "CERTIFICATE OF COMPLETION", font=_font(58, True), fill="#173b4f", anchor="mm")
    draw.text((width // 2, 405), "This certificate is proudly presented to", font=_font(28), fill="#4e5960", anchor="mm")
    draw.text((width // 2, 520), user["name"], font=_font(66, True), fill="#9a7026", anchor="mm")
    draw.line((300, 575, width - 300, 575), fill="#c39b4a", width=2)
    draw.text((width // 2, 655), "for successfully completing the 5-Day Internet Basics Course", font=_font(27), fill="#4e5960", anchor="mm")
    draw.text((width // 2, 715), f"Quiz score: {percentage:.0f}%", font=_font(28, True), fill="#173b4f", anchor="mm")

    issue_date = datetime.now().strftime("%d %B %Y")
    draw.text((250, 885), issue_date, font=_font(24, True), fill="#173b4f", anchor="mm")
    draw.line((135, 850, 365, 850), fill="#8c969b", width=2)
    draw.text((250, 925), "Date issued", font=_font(20), fill="#59666c", anchor="mm")

    draw.line((width - 470, 850, width - 170, 850), fill="#8c969b", width=2)
    draw.text((width - 320, 885), "Course Instructor", font=_font(22, True), fill="#173b4f", anchor="mm")
    draw.text((width - 320, 925), "Internet Basics", font=_font(20), fill="#59666c", anchor="mm")

    learner_id = user.get("id", "")
    certificate_id = f"IB-{learner_id}-{datetime.now():%Y%m%d}"
    qr = qrcode.make(f"Internet Basics certificate: {certificate_id}").convert("RGB")
    qr.thumbnail((150, 150))
    image.paste(qr, (width - 245, 110))
    draw.text((width - 170, 275), certificate_id, font=_font(14), fill="#59666c", anchor="mm")
    return image


def create_pdf(image):
    image_buffer = BytesIO()
    image.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    pdf_buffer = BytesIO()
    page_width, page_height = landscape(A4)
    document = canvas.Canvas(pdf_buffer, pagesize=(page_width, page_height))
    document.drawImage(
        ImageReader(image_buffer),
        0,
        0,
        width=page_width,
        height=page_height,
        preserveAspectRatio=True,
        anchor="c",
    )
    document.showPage()
    document.save()
    return pdf_buffer.getvalue()


def render_certificate(user):
    st.title("Certificate")
    try:
        statistics = database.get_quiz_statistics(user["id"])
    except Exception as error:
        st.error(f"Could not check quiz results: {error}")
        return

    percentage = float(statistics.get("best_percentage") or 0)
    if percentage < 70:
        st.warning("Pass the quiz with at least 70% to unlock your certificate.")
        if st.button("Take the quiz"):
            st.session_state.page = "quiz"
            st.rerun()
        return

    image = create_certificate_image(user, percentage)
    st.image(image, caption="Your Internet Basics course certificate", width="stretch")

    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", user["name"]).strip("_") or "learner"
    png_buffer = BytesIO()
    image.save(png_buffer, format="PNG")
    download_columns = st.columns(2)
    download_columns[0].download_button(
        "Download certificate PNG",
        data=png_buffer.getvalue(),
        file_name=f"internet_basics_certificate_{safe_name}.png",
        mime="image/png",
        width="stretch",
    )
    download_columns[1].download_button(
        "Download PDF / Print",
        data=create_pdf(image),
        file_name=f"internet_basics_certificate_{safe_name}.pdf",
        mime="application/pdf",
        width="stretch",
    )