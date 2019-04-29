import base64
import random
import string

import jwt
from flask_login import current_user

from config.encryption import SECRET_KEY
from flask import jsonify
from dao.user import UsersDAO
import pickle

#from handler.client import ClientHandler
from handler.newEmail import EmailHandler


class UsersHandler:

    def __init__(self):
        self.user_attributes = ['uid', 'fName', 'lName', 'email', 'pNumber', 'orderby']

    def build_user_dict(self, row):
        result = {}
        result['uid'] = row[0]
        result['FName'] = row[1]
        result['LName'] = row[2]
        result['Email'] = row[3]
        result['PNumber'] = row[4]
        return result

    def build_profile_dict(self, row):
        result = {}
        result['Name'] = row[1]
        result['Last Name'] = row[2]
        result['Email'] = row[3]
        result['Phone Number'] = row[4]
        return result

    def insert(self, form, Role):
        try:
            FName = form['FName']
            LName = form['LName']
            password = form['password']
            PNumber = form['PNumber']
            Email = form['Email']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
        uDao = UsersDAO()

        if FName and LName and password and PNumber and Email and Role:
            try:
                uID = uDao.insert(FName, LName, password, PNumber, Email, Role)   #INSERT #1

            except Exception as e:
                raise e

            return uID
        else:
            return jsonify(Error="Null values in user creation request."), 400

    '''
    def getUser(self,form):
        uDao = UsersDAO()

        filteredArgs = {}
        for arg in form:
            if form[arg] and arg in self.worker_attributes:
                if arg != 'orderby':
                    filteredArgs[arg] = form[arg]
                elif form[arg] in self.orderBy_attributes:
                    filteredArgs[arg] = form[arg]

        if not args:
            user = uDao.getAllUsers()
        for arg in args:
            if not arg in self.user_attributes:
                return jsonify(Error="Invalid Argument"), 401

        if not 'orderby' in args:
            worker_list = uDao.getUserByArguments(args)

        elif ((len(args)) == 1) and 'orderby' in args:
            worker_list = uDao.getUserWithSorting(args.get('orderby'))

        else:
            worker_list = uDao.getUserByArgumentsWithSorting(args)

        result_list = []

        for row in worker_list:
            result = self.build_worker_dict(row)
            result_list.append(result)

        return jsonify(Inventory=result_list)
    '''
    
    def updateName(self, form):
        uDao = UsersDAO()
        email = current_user.email
        uName = form['FName']
        uLName = form['LName']

        if len(form) != 3:
            return jsonify(Error="Malformed update request."), 400
        else:
            if uName and uLName:
                uDao.updateName(email, uName, uLName)
            else:
                return jsonify(Error="No attributes in update request"), 400

            row = uDao.getUserByEmail(email)
            result = self.build_worker_dict(row)
            return jsonify(User=result)

    def updatePassword(self, form):     #When User is logged in
        uDao = UsersDAO()
        password = form['newPassword']
        email = current_user.email

        if not uDao.getUserByEmail(email):
            return jsonify(Error="User not found."), 404
        else:
            uDao.updatePassword(email, password)
            return jsonify("Password has been updated")



    def updatePNumber(self, form):
        uDao = UsersDAO()
        email = current_user.email
        try:
            pNumber = form['PNumber']
        except Exception as e:
            return jsonify(Error="An error has occurred. please verify the submitted arguments.")

        if not uDao.getUserByEmail(email):
            return jsonify(Error="An error has occurred."), 400

        uDao.updatePNumber(email, pNumber)

        row = uDao.getUserByEmail(email)
        result = self.build_user_dict(row)
        return jsonify(User=result)

    def getUserWithCID(self, cid):
        uDao = UsersDAO()
        row = uDao.getUserWithCID(cid)
        if not row:
            return jsonify(Error="User not found."), 400
        else:
            user = self.build_user_dict(row)
            return jsonify(user)

    def getUserByEmail(self, email):
        uDao = UsersDAO()
        result = uDao.getUserByEmail(email)
        return result

    def getProfile(self, email):
        uDao = UsersDAO()
        row = uDao.getUserByEmail(email)
        result = self.build_profile_dict(row)
        return result

    def getUserIDByEmail(self, Email):
        uDao = UsersDAO()
        uid = uDao.getUserIDByEmail(Email)
        return uid

    def getUserWithWID(self, wid):
        uDao = UsersDAO()
        row = uDao.getUserWithWID(wid)
        if not row:
            return jsonify(Error="User not found."), 400
        else:
            user = self.build_user_dict(row)
            return jsonify(user)

    def addToLoginAttempt(self, email):
        uDao = UsersDAO()
        attempts = uDao.getLoginAttempts(email)
        attempts = attempts + 1
        uDao.addToLoginAttempt(email, attempts)


    def resetLoginAttempt(self, email):
        uDao = UsersDAO()
        uDao.resetLoginAttempt(email)

    def getBlockTime(self, email):
        uDao = UsersDAO()
        bTime = uDao.getBlockTime(email)
        return bTime

    def setBlockTime(self, email):
        uDao = UsersDAO()
        uDao.setBlockTime(email)

    def getConfirmation(self, email):
        uDao = UsersDAO()
        state = uDao.getConfirmation(email)
        return state

    def getLoginAttempts(self, email):
        uDao = UsersDAO()
        attempts = uDao.getLoginAttempts(email)
        return attempts


    def getUserInfo(self, email, role):
        uDao = UsersDAO()
        user = uDao.getUserInfo(email, role)
        return user

    def checkCurrentPassword(self, email, oldPassword):
        uDao = UsersDAO()
        validation = uDao.checkCurrentPassword(email, oldPassword)
        return validation

    def getPhoneNumberByUID(self, reqID):
        uDao = UsersDAO()
        user = uDao.getPhoneNumberByUID(reqID)
        return user

    def confirmAccount(self, args):
        token = args.get('value')
        try:
            data = jwt.decode(token, SECRET_KEY)
            email = data['Email']
        except:
            return jsonify(Error="Malformed request."), 404

        if not email:
            return jsonify("An error has occurred."), 400

        uDao = UsersDAO()
        uid = uDao.confirmAccount(email)
        if uid is None:
            return jsonify("An error has occurred."), 400
        return jsonify("Account was successfully confirmed.")

    def confirmForgotPassword(self, form):
        try:
            email = form['Email']
        except Exception as e:
            return jsonify("An error has occurred."), 400

        if not email:
            return jsonify("An error has occurred."), 400

        uid = self.getUserIDByEmail(email)

        if not uid:
            return jsonify("An error has occurred."), 400
        try:
            eHand = EmailHandler()
            eHand.confirmResetPassword(email)
        except Exception as e:
            return jsonify("An error has occurred."), 400

        return jsonify("An email has been sent to the provided address.")

    def resetPassword(self, args):
        token = args.get('value')
        try:
            data = jwt.decode(token, SECRET_KEY)
            email = data['Email']
        except:
            return jsonify(Error="An error has occurred."), 404

        uDao = UsersDAO()
        if not uDao.getUserByEmail(email):
            return jsonify(Error="An error has occurred."), 400
        else:
            valid = True
            while valid:
                password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
                size = len(password)
                if size >= 8 \
                    and any(a.islower() for a in password) \
                    and any(a.isupper() for a in password) \
                    and any(a.isnumeric() for a in password):
                    valid = False
            print(password)
            try:
                uDao.updateForgottenPassword(email, password)
                return jsonify("An email has been sent to the provided address.")
            except Exception as e:
                return jsonify("An error has occurred.")

    def newConfirmation(self, form):
        uHand = UsersHandler()
        email = form['Email']
        if not email:
            return jsonify(Error="An error has occurred."), 401

        confirmation = uHand.getConfirmation(email)
        if confirmation is True:
            return jsonify(Error="An error has occured."), 401
        elif confirmation is None:
            return jsonify(Error="An error has occurred."), 403
        else:
            eHand = EmailHandler()
            try:
                eHand.confirmationEmail(email)
                return jsonify("An email has been sent to the provided address.")
            except Exception as e:
                return jsonify(Error="An error has occurred.")
