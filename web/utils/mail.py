from flask import render_template
from flask_mail import Message, Mail
from config import mail_sender
from functools import partial

mail = Mail()
def send_email(to, subject, email_token, error_message = None, error_code = None):
    try:
        send_registration_email(
            to=form['email'],
            email_token=email_token,
            subject=form['username']
        )
    except SMTPException:
        return jsonify(message = error_message), error_code

send_registration_email = partial(send_email,
                                  error_message = 'Something went wrong for sent email',
                                  error_code = 512)

send_email_change_pass = partial(send_email,
                                  error_message = 'Something went wrong',
                                  error_code = 500)


