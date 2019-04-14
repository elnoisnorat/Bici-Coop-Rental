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
from handler.sendEmail import EmailHandler


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
        FName = form['FName']
        LName = form['LName']
        password = form['password']
        PNumber = form['PNumber']
        Email = form['Email']
        uDao = UsersDAO()

        if FName and LName and password and PNumber and Email and Role:
            try:
                uID = uDao.insert(FName, LName, password, PNumber, Email, Role)   #INSERT #1
            except Exception as e:
                raise e

            return uID
        else:
            return jsonify(Error="Null values in user creation request."), 400

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
    
    def updateName(self, form):
        uDao = UsersDAO()
        email = current_user.email
        #email = form['email']
        uName = form['FName']
        uLName = form['LName']

        if not email:
            return jsonify(Error="No email given")

        if not uDao.getUserByEmail(email):
            return jsonify(Error="User not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request."), 400
            else:
                if uName and uLName:
                    uDao.updateName(email, uName, uLName)
                else:
                    return jsonify(Error="No attributes in update request"), 400

                row = uDao.getUserByEmail(email)
                result = self.build_worker_dict(row)
                return jsonify(User=result), 200

    def updatePassword(self, form):     #When User is logged in

        uDao = UsersDAO()
        #token = form['token']
        password = form['password']
        email = current_user.email

        if not uDao.getUserByEmail(email):
            return jsonify(Error="User not found."), 404
        else:
            if password:
                uDao.updatePassword(email, password)
                return jsonify("Password has been updated")
            else:
                return jsonify(Error="No attributes in update request"), 400


    def updatePNumber(self, form):
        uDao = UsersDAO()

        email = current_user.email
        pNumber = form['PNumber']

        if not uDao.getUserByEmail(email):
            return jsonify(Error="User not found."), 404

        if pNumber:
            uDao.updatePNumber(email, pNumber)
        else:
            return jsonify(Error="No attributes in update request"), 400

        row = uDao.getUserByEmail(email)
        result = self.build_user_dict(row)
        return jsonify(User=result), 200

    def getUserWithCID(self, cid):
        uDao = UsersDAO()
        row = uDao.getUserWithCID(cid)
        if not row:
            return jsonify(Error="User not found.")
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
            return jsonify(Error="User not found.")
        else:
            user = self.build_user_dict(row)
            return jsonify(user)

    def confirmAccount(self, args):
        value = args.get('value')
        print(value)
        #uID = pickle.loads(value.decode('base64', 'strict'))
        #code = package['code']
        uDao = UsersDAO()
        uDao.confirmAccount(value)
        return jsonify("Account was successfully activated.")

    def resetPassword(self, form):
        email = form['Email']
        uDao = UsersDAO()
        if not uDao.getUserByEmail(email):
            return jsonify(Error="User does not exist."), 404
        else:
            password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
            eHand = EmailHandler()

            uDao.updatePassword(email, password)
            eHand.resetPassword(email, password)

            return jsonify("Email has been sent.")

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





