from flask_login import current_user

from dao.client import ClientDAO
from handler.user import UsersHandler
from dao.user import UsersDAO
from config.encryption import SECRET_KEY
from flask import jsonify
import jwt
import datetime

class ClientHandler:

    def __init__(self):
        self.client_attributes = ['FName', 'LName', 'PNumber', 'cid', 'uid', 'debtorflag', 'orderby']
        self.orderBy_attributes = ['fName', 'lName', 'pNumber', 'cid', 'uid', 'debtorflag']

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

                cDao = ClientDAO()
                cID = cDao.clientLogin(email, password)
                if not cID:
                    uHand.addToLoginAttempt(email)
                    return -2

                uHand.resetLoginAttempt(email)

                token = jwt.encode({'Role': 'Client', 'cID': cID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, SECRET_KEY)
                userInfo = uHand.getProfile(email)
                userInfo['Role'] = 'Client'

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
            uID = uHandler.insert(form, 'Client')
        except Exception as e:
            raise e
        cDao = ClientDAO()
        cID = cDao.getClientByUID(uID)
        return jsonify("Client #: " + str(cID) + " was successfully added.")

    def getClient(self, form):
        cDao = ClientDAO()

        filteredArgs = {}
        for arg in form:
            if form[arg] and arg in self.client_attributes:
                if arg != 'orderby':
                    filteredArgs[arg] = form[arg]
                elif form[arg] in self.orderBy_attributes:
                    filteredArgs[arg] = form[arg]

        if len(filteredArgs) == 0:
            client_list = cDao.getAllClients()

        if not 'orderby' in filteredArgs:
            client_list = cDao.getClientByArguments(filteredArgs)

        elif ((len(filteredArgs)) == 1) and 'orderby' in filteredArgs:
            client_list = cDao.getClientWithSorting(filteredArgs['orderby'])

        else:
            client_list = cDao.getClientByArgumentsWithSorting(filteredArgs)

        result_list = []

        for row in client_list:
            result = self.build_client_dict(row)
            result_list.append(result)

        return jsonify(Clients=result_list)

    def updatePassword(self, form):
        uDao = UsersHandler.updatePassword()                                                #Update #1

    def getClientByCID(self, cid):
        cDao = ClientDAO()
        row = cDao.getClientByCID(cid)
        return row

    def getClientByUID(self, uID):
        cDao = ClientDAO()
        cID = cDao.getClientByUID(uID)

