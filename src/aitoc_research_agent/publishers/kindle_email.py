from __future__ import annotations

import mimetypes
import smtplib
from email.message import EmailMessage
from pathlib import Path


def send_to_kindle(
    *,
    smtp_host: str,
    smtp_port: int,
    smtp_username: str,
    smtp_password: str,
    sender_email: str,
    kindle_email: str,
    attachment_path: Path,
    subject: str,
) -> None:
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = kindle_email
    message["Subject"] = subject
    message.set_content("Attached research export for Kindle.")

    content_type, _ = mimetypes.guess_type(str(attachment_path))
    if content_type is None:
        content_type = "application/octet-stream"
    maintype, subtype = content_type.split("/", 1)
    message.add_attachment(
        attachment_path.read_bytes(),
        maintype=maintype,
        subtype=subtype,
        filename=attachment_path.name,
    )

    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(message)

