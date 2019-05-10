import traceback

import datetime

import jwt
# from flask import current_app as app
from app import app
from flask_mail import Mail, Message
from config.account import EMAIL, PASSWORD, AWS_LINK
from config.encryption import SECRET_KEY

app.config['DEBUG']= True
app.config['TESTING']= False
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= 465
app.config['MAIL_USE_TLS']= False
app.config['MAIL_USE_SSL']= True
app.config['MAILS_DEBUG']= True
app.config['MAIL_USERNAME']= EMAIL
app.config['MAIL_PASSWORD']= PASSWORD
app.config['MAIL_DEFAULT_SENDER']= EMAIL
app.config['MAIL_MAX_EMAIL']= 2
app.config['MAIL_SUPRESS_SEND']= False
app.config['MAIL_ASCII_ATTACHMENTS']= False
web_link = AWS_LINK

mail = Mail(app)
class EmailHandler():
    def confirmationEmail(self, email):
        token = jwt.encode({'Email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, SECRET_KEY)
        content = str(token)
        link = AWS_LINK + "/confirm?value=" +str(content[2:len(content)-1])
        msg = Message('Account Confirmation', recipients=[email])
        body = '''Please click <a href="''' + link + '''"> here</a> to confirm your account.'''
        msg.html = body
        try:
            mail.send(msg)
            return "Confirmation email has been sent to the provided email. Please confirm your email within 24 hours."
        except Exception as e:
            raise e

    def confirmResetPassword(self, email):
        token = jwt.encode({'Email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, SECRET_KEY)
        print(email)
        print(token)
        content = str(token)
        link = AWS_LINK + "/forgotPassword?value=" + str(content[2:len(content)-1])
        msg = Message('Password Recovery Confirmation', recipients=[email])
        body = '''A request for a new password has been made for this account. 
        Click <a href="''' + link + '''"> here</a> to receive a new password. 
        If you did not issue this request, please ignore this message.
        '''
        msg.html = body

        try:
            mail.send(msg)
        except Exception as e:
            raise e

    def resetPassword(self, email, password):

        content = password
        msg = Message('Password Recovery', recipients=[email])
        msg.body = "Here is your new password: " + content + ". Please login to your account and set a new password."
        try:
            mail.send(msg)
            return "TEST COMPLETED"
        except Exception as e:
            traceback.print_exc()
            raise e
