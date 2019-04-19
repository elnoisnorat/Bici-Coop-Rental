from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config.encryption import SECRET_KEY

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = SECRET_KEY