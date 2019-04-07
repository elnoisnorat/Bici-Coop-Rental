from flask import jsonify
from dao.user import UsersDAO
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

    def insert(self, form):
        '''
        if len(form) != 5:
            return jsonify(Error="Malformed post request"), 400
        else:
        '''
        FName = form['FName']
        LName = form['LName']
        password = form['password']
        PNumber = form['PNumber']
        Email = form['Email']
        uDao = UsersDAO()

        if uDao.getUserByEmail(Email):
            return jsonify("User already exists")

        if FName and LName and password and PNumber and Email:
            uID = uDao.insert(FName, LName, password, PNumber, Email)
            return uID
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def getUser(self,form):
        uDao = UsersDAO()

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

        email = form['email']
        uName = form['FName']
        uLName = form['LName']

        if not email:
            return jsonify(Error="No worker id given")

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

    def updatePassword(self, form):
        uDao = UsersDAO()

        email = form['email']
        password = form['password']

        if not email:
            return jsonify(Error="No user email given")

        if not uDao.getUserByEmail(email):
            return jsonify(Error="User not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request."), 400
            else:
                if password:
                    uDao.updateName(email, password)
                else:
                    return jsonify(Error="No attributes in update request"), 400

                row = uDao.getUserByEmail(email)
                result = self.build_worker_dict(row)
                return jsonify(User=result), 200

    def updatePNumber(self, form):
        uDao = UsersDAO()

        email = form['email']
        pNumber = form['pNumber']

        if not email:
            return jsonify(Error="No worker email given")

        if not uDao.getUserByEmail(email):
            return jsonify(Error="User not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request."), 400
            else:
                if pNumber:
                    uDao.updatePNumber(email, pNumber)
                else:
                    return jsonify(Error="No attributes in update request"), 400

                row = uDao.getUserByEmail(wid)
                result = self.build_worker_dict(row)
                return jsonify(User=result), 200

    def getUserWithCID(self, cid):
        uDao = UsersDAO()
        row = uDao.getUserWithCID(cid)
        if not row:
            return jsonify(Error="User not found.")
        else:
            user = self.build_user_dict(row)
            return jsonify(user)

    def getUserByEmail(self, Email):
        uDao = UsersDAO()
        result = uDao.getUserByEmail(Email)
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
