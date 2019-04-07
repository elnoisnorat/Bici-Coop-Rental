from dao.client import ClientDAO
from handler.user import UsersHandler
from dao.user import UsersDAO
from config.encryption import SECRET_KEY
from flask import jsonify
import jwt
import datetime

class ClientHandler:

    def build_client_dict(self, row):
        result = {}
        result['cID'] = row[0]
        result['fName'] = row[1]
        result['lName'] = row[2]
        return result

    def clientLogin(self, form):
        email = form['Email']
        password = form['password']
        if email and password:
            cDao = ClientDAO()
            cID = cDao.clientLogin(email, password)
            token = jwt.encode({'Role': 'Client', 'cID': cID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, SECRET_KEY)
            response = {
                'token': token.decode('UTF-8')
            }
            return jsonify(response)
        else:
            return jsonify(Error="Invalid username or password."), 401

    def insert(self, form):
        print(form)
        if len(form) != 5:
            print(len(form))
            return jsonify(Error="Malformed request")

        else:
            #Email = form['Email']
            #uHandler = UsersHandler()
            cDao = ClientDAO()
            #uid = uHandler.getUserIDByEmail(Email)

            #if not uid:
                #uid = uHandler.insert(form)

            #if cDao.getClientByUID(uid):
                #return jsonify(Error="User is already a Client")
            #if uid:
            try:
                cID = cDao.insert(form)
                pass
            except Exception as e:
                return jsonify(Error="Insert Failed")
            return jsonify("Client #: " + str(cID) + " was successfully added.")
            #else:
             #   return jsonify(Error="Null value in attributes of the client."), 401

    def getClient(self, args):
        uDao = UsersDAO()
        if not args:
            user = uDao.getAllUsers()
        for arg in args:
            if not arg in self.user_attributes:
                return jsonify(Error="Invalid Argument"), 401

        if not 'orderby' in args:
            user_list = uDao.getUserByArguments(args)

        elif ((len(args)) == 1) and 'orderby' in args:
            user_list = uDao.getUserWithSorting(args.get('orderby'))

        else:
            user_list = uDao.getUserByArgumentsWithSorting(args)

        result_list = []

        for row in user_list:
            result = self.build_user_dict(row)
            result_list.append(result)

        return jsonify(Inventory=result_list)

    def updatePassword(self, form):
        uDao = UsersHandler.updatePassword()

    def getClientByCID(self, cid):
        cDao = ClientDAO()
        row = cDao.getClientByCID(cid)
        return row

    def getClientByUID(self, uID):
        cDao = ClientDAO()
        cID = cDao.getClientByUID(uID)

