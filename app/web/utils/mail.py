import os
from flask import render_template
from flask_mail import Message, Mail

mail_sender = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail()


def send_registration_email(to, subject, email_token):
    msg = Message(
        subject,
        recipients=[to],
        html=render_template('/email_registration.html', email_token=email_token, subject=subject),
        sender=mail_sender
    )
    mail.send(msg)


def send_email_change_pass(to, subject, email_token):
    msg = Message(
        subject,
        recipients=[to],
        html=render_template('/email_change_pass.html', email_token=email_token, subject=subject),
        sender=mail_sender
    )
    mail.send(msg)
