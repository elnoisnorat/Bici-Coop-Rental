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
        if email and password:                                              #No null arguments
            confirmation = uHand.getConfirmation(email)
            if confirmation is False or confirmation is None:                                      #User does not exist
                return -2

            attempts = uHand.getLoginAttempts(email)                        #Get current number of attempts
            blockTime = uHand.getBlockTime(email)                           #Get current account block time

            if datetime.datetime.now() > blockTime:                         #If current time > block time proceed

                if attempts == 7:
                    uHand.setBlockTime(email)                               #Lock account at 7 attempts
                    return -1

                aDao = AdminDAO()
                aID = aDao.adminLogin(email, password)                      #Validate User
                if not aID:
                    uHand.addToLoginAttempt(email)                          #Add to login attempt
                    return -2

                uHand.resetLoginAttempt(email)                              #Set login attempt to 0

                userInfo = uHand.getProfile(email)                          #Get User information

                response = {
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
            uID = uHandler.insert(form, "Admin")                             #Try to insert a new user with role admin
        except Exception as e:
            return jsonify(Error="An error has occurred."), 400
        aDao = AdminDAO()
        aID = aDao.getAdminByUID(uID)
        return jsonify("Admin #: " + str(aID) + " was successfully added.")
