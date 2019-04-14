from flask import jsonify
from config.encryption import SECRET_KEY, ENC_ALG
from dao.admin import AdminDAO
from handler.user import UsersHandler
from dao.user import UsersDAO
import jwt
import datetime

class AdminHandler:

    def adminLogin(self, form):
        uHand = UsersHandler()
        email = form['Email']
        password = form['password']
        if email and password:
            confirmation = uHand.getConfirmation(email)
            if confirmation is False:
                return jsonify("Email has not been confirmed yet.")
            elif confirmation is None:
                return -2

            attempts = uHand.getLoginAttempts(email)
            blockTime = uHand.getBlockTime(email)

            if datetime.datetime.now() > blockTime:

                if attempts == 7:
                    uHand.setBlockTime(email)
                    return -1

                aDao = AdminDAO()
                aID = aDao.adminLogin(email, password)
                if not aID:
                    uHand.addToLoginAttempt(email)
                    return -2

                uHand.resetLoginAttempt(email)

                token = jwt.encode({'Role': 'Admin', 'aID': aID, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, SECRET_KEY)
                userInfo = uHand.getProfile(email)

                response = {
                    'token': token.decode('UTF-8'),
                    'info' : userInfo
                }
                return jsonify(response)
            else:
                return -1
        else:
            return -2

    def insert(self, form):
        uHandler = UsersHandler()
        try:
            uID = uHandler.insert(form, "Admin")
        except Exception as e:
            raise e
        aDao = AdminDAO()
        aID = aDao.getAdminByUID(uID)
        return jsonify("Admin #: " + str(aID) + " was successfully added.")

    '''
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
    '''

    def getAdmin(self):
        return ''

