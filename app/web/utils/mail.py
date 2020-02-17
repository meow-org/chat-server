import os
from flask import render_template
from flask_mail import Message, Mail
from ..config import BASE_URL_APP

mail_sender = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail()


def create_url(url, **kwargs):
    new_url_arr = []
    url_arr = url.split('/')

    for dt in url_arr:
        url_el = dt.split(':')
        if len(url_el) == 2:
            if kwargs and kwargs[url_el[1]]:
                new_url_arr.append(str(kwargs[url_el[1]]))
                continue
        new_url_arr.append(dt)

    return BASE_URL_APP + '/'.join(new_url_arr)


def send_registration_email(to, subject, email_token):
    reg_html = render_template(
        '/email_registration.html',
        url=create_url('/validate-email/:email_token',
                       email_token=email_token),
        subject=subject)
    msg = Message(subject, recipients=[to], sender=mail_sender, html=reg_html)
    mail.send(msg)


def send_email_change_pass(to, subject, email_token):
    change_pass_html = render_template(
        '/email_change_pass.html',
        url=create_url(
            '/validate-password/:email/:email_token',
            email_token=email_token,
            email=to),
        subject=subject)
    msg = Message(subject, recipients=[to], html=change_pass_html, sender=mail_sender)
    mail.send(msg)
