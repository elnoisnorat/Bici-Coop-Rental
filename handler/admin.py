from flask import jsonify
from config.encryption import SECRET_KEY, ENC_ALG
from dao.admin import AdminDAO
from handler.user import UsersHandler
from dao.user import UsersDAO
import jwt
import datetime

class AdminHandler:

    def adminLogin(self, form):
        '''
        Method used for admin login
        :param form: request.json
        :return: A response object containing the user's name, last name, phone number and email
        '''
        uHand = UsersHandler()
        email = form['Email']
        password = form['password']
        if email and password:                                              #No null data
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
        '''
        Method used to create a new user. Calls the UserHandler().insert() method
        :param form: request.json
        :return: A response object with a message confirming account creation
        '''
        uHandler = UsersHandler()
        if uHandler.getUserIDByEmail(form['Email']) is not None:
            return jsonify(Error="Please use another email address."), 400
        try:    #Try to insert a new user with role admin
            uHandler.insert(form, "Admin")
        except Exception as e:  #Catch an exception during the creation process
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
        return jsonify("Account was successfully created.")
