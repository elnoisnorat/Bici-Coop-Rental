
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import base64
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config.encryption import EMAIL_KEY

class EmailHandler:
    def confirmationEmail(self, email, uid):

        #code_64 = pickle.dumps(email).encode('base64', 'strict')
        # token = jwt.encode({'Role': 'Admin', 'aID': aID, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, SECRET_KEY)

        link = "localhost:5000/confirm?value=" + uid
        content = '''Please click <a href="''' + link + '''">here.</a>'''
        message = Mail(
            from_email='',
            to_emails=email,
            subject='Account Confirmation',
            html_content=content)
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
        print(email)
        print(content)
        message = Mail(
            from_email='',
            to_emails= email,
            subject='Password Recovery',
            html_content = "Here is your new password: " + content +
                           ". Please login to your account and set a new password.")
        try:
            sg = SendGridAPIClient(EMAIL_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)