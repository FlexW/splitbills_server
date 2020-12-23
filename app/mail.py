from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    mail_subject_prefix = current_app.config["MAIL_SUBJECT_PREFIX"]
    sender = current_app.config["MAIL_SENDER"]

    msg = Message(mail_subject_prefix + " " + subject,
                  sender=sender,
                  recipients=[to],
                  body=render_template(template + ".txt", **kwargs),
                  html=render_template(template + ".html", **kwargs))

    thread = Thread(target=send_mail_async, args=[app, msg])
    thread.start()

    return thread


def send_mail_async(app, msg):
    with app.app_context():
        mail.send(msg)
