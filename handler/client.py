from flask_login import current_user

from dao.client import ClientDAO
from handler.user import UsersHandler
from flask import jsonify
import jwt
import datetime

class ClientHandler:

    def __init__(self):
        self.client_attributes = ['FName', 'LName', 'PNumber', 'cid', 'uid', 'debtorflag', 'orderby']
        self.orderBy_attributes = ['fName', 'lName', 'pNumber', 'cid', 'uid', 'debtorflag']
        self.attempts = 0

    def build_client_dict(self, row):
        result = {}
        result['cID'] = row[0]
        result['fName'] = row[1]
        result['lName'] = row[2]
        result['Email'] = row[3]
        result['Phone Number'] = row[4]
        result['Debtor Flag'] = row[5]
        return result

    def clientLogin(self, form):
        uHand = UsersHandler()
        email = form['Email']
        password = form['password']
        if email and password:                                                  #No null arguments
            confirmation = uHand.getConfirmation(email)
            if confirmation is False or confirmation is None:                                          #User does not exist
                return -2

            attempts = uHand.getLoginAttempts(email)                            #Get current number of attempts
            blockTime = uHand.getBlockTime(email)                               #Get current account block time

            if datetime.datetime.now() > blockTime:                             #If current time > block time proceed

                if attempts == 7:
                    uHand.setBlockTime(email)                                   #Lock account at 7 attempts
                    return -1

                cDao = ClientDAO()
                cID = cDao.clientLogin(email, password)                         #Validate User
                if not cID:
                    uHand.addToLoginAttempt(email)                              #Add to login attempt
                    return -2

                uHand.resetLoginAttempt(email)                                  #Set login attempt to 0

                userInfo = uHand.getProfile(email)                              #Get User information

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
            uID = uHandler.insert(form, 'Client')                               #Try to insert a new user with role admin
        except Exception as e:
            return jsonify(Error="An error has occurred."), 400
        return jsonify("Account was successfully created.")

    def getClient(self, form):
        cDao = ClientDAO()

        filteredArgs = {}
        for arg in form:                                                        #Filter arguments received using a dictionary
            if form[arg] and arg in self.client_attributes:
                if arg != 'orderby':
                    filteredArgs[arg] = form[arg]
                elif form[arg] in self.orderBy_attributes:
                    filteredArgs[arg] = form[arg]

        if len(filteredArgs) == 0:                                              #No arguments given getAll()
            client_list = cDao.getAllClients()

        elif not 'orderby' in filteredArgs:                                       #If no order by give list without order
            client_list = cDao.getClientByArguments(filteredArgs)

        elif ((len(filteredArgs)) == 1) and 'orderby' in filteredArgs:          #If order by with no other arguments getAll() ordered
            client_list = cDao.getClientWithSorting(filteredArgs['orderby'])

        else:
            client_list = cDao.getClientByArgumentsWithSorting(filteredArgs)    #If order by give list with order

        result_list = []

        for row in client_list:                                                 #Build dictionary
            result = self.build_client_dict(row)
            result_list.append(result)

        return jsonify(Clients=result_list)

    # def updatePassword(self, form):
    #     uDao = UsersHandler.updatePassword()                                                #Update #1

    def getClientByCID(self, cid):
        cDao = ClientDAO()
        row = cDao.getClientByCID(cid)
        return row

    def getClientByUID(self, uID):
        cDao = ClientDAO()
        client = cDao.getClientByUID(uID)
        return client

    def getCIDByUID(self, reqID):
        cDao = ClientDAO()
        cID = cDao.getCIDByUID(reqID)
        return cID

