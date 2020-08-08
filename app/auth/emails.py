import secrets
import os
from flask import url_for, current_app, render_template
from flask_mail import Message
from app import mail
from threading import Thread
from time import sleep 
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)



def send_email(user, type):
    token = user.generate_token()
    subject = ""
    body = ""
    if type == "confirmation":
        subject = '[Bloggers]Email Confirmation Request'
        body = f'''To activate your account, visit the following link:
        { url_for('users.confirm_mail', token=token, _external=True) }
        If you did not make this request then simply ignore this email and no changes will be made.
        '''
    else:
        subject = '[Bloggers]Password Reset Request'
        body = f'''To reset your password, visit the following link:
        {url_for('users.reset_token', token=token, _external=True)}
        If you did not make this request then simply ignore this email and no changes will be made.
        '''
    print(subject + "\n" + body)
    msg=Message(subject,
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user.email],
                )
    msg.body = body
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_change_email(user,email):
    token = user.generate_email_change_token(email)
    msg=Message('[Bloggers]Email Confirmation Request',
                sender=os.environ.get('MAIL_USERNAME'),
                recipients=[email],
                )
    msg.body = f'''To change your email, visit the following link:
    { url_for('users.change_email', token=token, _external=True) }
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    thr = Thread(target=send_async_email, args=[current_app, msg])
    thr.start()
    return thr


def send_reset_email(user):
    token = user.generate_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    thr = Thread(target=send_async_email, args=[current_app, msg])
    thr.start()
    return thr 