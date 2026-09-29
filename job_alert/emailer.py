import os
import smtplib
from email.message import EmailMessage
from html import escape


def send_email(jobs):
    username = os.environ["MAIL_USERNAME"]
    password = os.environ["MAIL_APP_PASSWORD"]
    recipient = os.environ["MAIL_TO"]

    subject = f"Engineering Job Alert — {len(jobs)} new match"
    if len(jobs) != 1:
        subject += "es"

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = username
    message["To"] = recipient

    text_parts = [
        f"{len(jobs)} new engineering job match(es) were found.\n"
    ]

    html_parts = [
        "<h2>New engineering job matches</h2>",
        f"<p>{len(jobs)} new match(es).</p>",
    ]

    for job, score in jobs:
        text_parts.append(
            f"""
{job.company}
{job.title}
Location: {job.location or 'Not specified'}
Score: {score}
Apply: {job.url}
"""
        )

        html_parts.append(
            f"""
            <hr>
            <h3>{escape(job.title)}</h3>
            <p><b>{escape(job.company)}</b><br>
            Location: {escape(job.location or 'Not specified')}<br>
            Match score: {score}</p>
            <p><a href="{escape(job.url)}">Open the company application page</a></p>
            """
        )

    message.set_content("\n".join(text_parts))
    message.add_alternative("\n".join(html_parts), subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(username, password)
        smtp.send_message(message)
