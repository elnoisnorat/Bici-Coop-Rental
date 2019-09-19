from flask import Flask, request, jsonify, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from apscheduler.schedulers.background import BackgroundScheduler
import time
import atexit

scheduler = BackgroundScheduler()

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# def job(number):
#     print("I'm working on #:" + str(number))
#
# def bye():
#     print("I HAVE SHUTDOWN.")
#
scheduler.start()
# scheduler.add_job(func=job,args = [4], trigger="interval", seconds=3)

# Shut down the scheduler when exiting the app
#atexit.register(lambda: scheduler.shutdown())
# atexit.register(bye)