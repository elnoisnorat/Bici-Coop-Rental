import datetime

import jwt
# from flask import current_app as app
from app import app
from flask_mail import Mail, Message

from config.encryption import SECRET_KEY

app.config['DEBUG']= True
app.config['TESTING']= False
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= 465
app.config['MAIL_USE_TLS']= False
app.config['MAIL_USE_SSL']= True
app.config['MAILS_DEBUG']= True
app.config['MAIL_USERNAME']= ''
app.config['MAIL_PASSWORD']= ''
app.config['MAIL_DEFAULT_SENDER']= ''
app.config['MAIL_MAX_EMAIL']= 1
app.config['MAIL_SUPRESS_SEND']= False
app.config['MAIL_ASCII_ATTACHMENTS']= False

mail = Mail(app)
class EmailHandler():
    def confirmationEmail(self, email):
        #link = "http://localhost:5000/confirm?value=" +  email
        token = jwt.encode({'Email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, SECRET_KEY)
        content = str(token)
        link = str(content[2:len(content)-1])
        msg = Message('Account Confirmation', recipients=[email])
        body = '''Please click localhost:5000/confirm?value=''' + link + '''email to confirm your account.'''
        msg.html = body
        try:
            mail.send(msg)
            return "TEST COMPLETED"
        except Exception as e:
            raise e

    def confirmResetPassword(self, email):
        token = jwt.encode({'Email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, SECRET_KEY)
        print(email)
        print(token)
        content = str(token)
        link = str(content[2:len(content)-1])
        '''A request for a new password has been made for this account. 
            Click to receive a new password. If you did not issue this request please ignore this message.
        '''
        msg = Message('Password Recovery', recipients=[email])
        msg.body = "localhost:5000/forgotPassword?value=" + link

        try:
            mail.send(msg)
            return "TEST COMPLETED"
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
            raise e
