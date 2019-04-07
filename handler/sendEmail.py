
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os

import pickle
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config.config import EMAIL_KEY

class EmailHandler:
    def confirmationEmail(self, email, uid, code):
        package = {
            "uID" : uid,
            "code" : code
        }

        code_64 = pickle.dumps(package).encode('base64', 'strict')
        link = ""
        content = '''Please click <a href="''' + link + '''">here</a>'''
        message = Mail(
            from_email='example',
            to_emails= email,
            subject='Account Confirmation',
            html_content = content)
        try:
            sg = SendGridAPIClient(EMAIL_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    def resetPassword(self, email, password):

        content = password

        message = Mail(
            from_email='example',
            to_emails= email,
            subject='Account Confirmation',
            html_content = content)
        try:
            sg = SendGridAPIClient(EMAIL_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)