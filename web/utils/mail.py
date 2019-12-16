from flask import render_template
from flask_mail import Message, Mail
from config import mail_sender

mail = Mail()


def send_email(to, subject, email_token):
    msg = Message(
        subject,
        recipients=[to],
        html=render_template('/send_email.html', email_token=email_token, subject=subject),
        sender=mail_sender
    )
    mail.send(msg)
