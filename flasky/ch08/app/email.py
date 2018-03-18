# -*- conding:utf-8 -*-
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwagrs):
    app=current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_REFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwagrs)
    msg.html = render_template(template + '.html', **kwagrs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr