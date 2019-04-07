from flask import jsonify
from config.encryption import SECRET_KEY, ENC_ALG
from dao.admin import AdminDAO
from handler.user import UsersHandler
from dao.user import UsersDAO
import jwt
import datetime

class AdminHandler:

    def adminLogin(self, form):
        email = form['email']
        password = form['password']
        if email and password:
            aDao = AdminDAO()
            aID = aDao.workerLogin(email, password)
            if not aID:
                return None
            token = jwt.encode({'Role': 'Admin', 'aID': aID, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 1)}, SECRET_KEY)

            uHand = UsersHandler()
            userInfo = uHand.getProfile(email)

            response = {
                'token': token.decode('UTF-8'),
                'info' : userInfo
            }
            return jsonify(response)
        else:
            return None

    def insert(self, form):
        email = form['Email']
        uHandler = UsersHandler()
        aDao = AdminDAO()
        uDao = UsersDAO()
        uid = uDao.getUserByEmail(email)
        if not uid:
            uid = uHandler.insert(form)                                                      #INSERT #1

        if aDao.getAdminByUID(uid):
            return jsonify(Error="User is already an Admin")
        if uid:
            aID = aDao.insert(uid)                                                           #INSERT #2
            return jsonify("Admin #: " + aID + " was successfully added.")
        else:
            return jsonify(Error="Null value in attributes of the admin."), 401

    def getAdmin(self):
        return ''

