from flask import request, jsonify
from functools import wraps
from flask_login import current_user
from dao.bicycle import BicycleDAO
from handler.user import UsersHandler


def isWorker(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != "Worker":
            return jsonify(Error="Unauthorized access."), 403

        return f(*args, **kwargs)
    return decorated

def isAdmin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != "Admin":
            return jsonify(Error="Unauthorized access."), 403
        return f(*args, **kwargs)
    return decorated

def isClient(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != "Client":
            return jsonify(Error="Unauthorized access."), 403
        return f(*args, **kwargs)
    return decorated

def isWorkerOrAdmin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != "Worker" and current_user.role != "Admin":
            return jsonify(Error="Unauthorized access."), 403
        return f(*args, **kwargs)
    return decorated

def isWorkerOrClient(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != "Worker" and current_user.role != "Client":
            return jsonify(Error="Unauthorized access."), 403
        return f(*args, **kwargs)
    return decorated



def hasRole(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != "Worker" and current_user.role != "Admin" and current_user.role != "Client":
            return jsonify(Error="Unauthorized access."), 403
        return f(*args, **kwargs)
    return decorated

def isDecomissioned(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        bDAO = BicycleDAO()
        bStatus = bDAO.getStatusByID(args[1])
        if bStatus == 'DECOMISSIONED':
            return jsonify(Error="This bicycle is decomissioned")
        return f(*args, **kwargs)
    return decorated

def validPassword(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        password = request.json['password']
        size = len(password)
        if size >= 8 \
                and any(a.islower() for a in password) \
                and any(a.isupper() for a in password) \
                and any(a.isnumeric() for a in password):
                pass
        else:
            return jsonify(Error="Password does not meet our standards."), 400
        return f(*args, **kwargs)
    return decorated

def validUpdatePassword(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            email = current_user.email
            uHand = UsersHandler()
            uid = uHand.getUserIDByEmail(email)
            password_list = []
            oldPassword = request.json['oldPassword']
            if not uHand.checkCurrentPassword(email, oldPassword):
                return jsonify(Error="Incorrect arguments."), 400 #############################

            newPassword = request.json['newPassword']
            confirmPassword = request.json['confirmPassword']
            if oldPassword != newPassword and newPassword == confirmPassword:
                password_list.append(oldPassword)
                password_list.append(newPassword)
                for password in password_list:
                    size = len(password)
                    if size >= 8 \
                            and any(a.islower() for a in password) \
                            and any(a.isupper() for a in password) \
                            and any(a.isnumeric() for a in password):
                        pass
                    else:
                        return jsonify(Error="Password does not meet our standards."), 400
            else:
                return jsonify(Error="Incorrect arguments."), 400
        except:
            return jsonify(Error="Incorrect arguments."), 400

        return f(*args, **kwargs)

    return decorated

def validPhoneNumber(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        pnumber = request.json['PNumber']
        size = len(pnumber)
        if size >= 10 and size <= 12 and pnumber.isnumeric():
            valid = True
        else:
            return jsonify(Error="Phone number does not meet our standards."), 400
        return f(*args, **kwargs)
    return decorated

def validUpdatePhoneNumber(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            oldPNumber = current_user.pNumber
            newPNumber = request.json['PNumber']

            if oldPNumber != newPNumber:
                size = len(newPNumber)
                if size >= 10 and size <= 12 and newPNumber.isnumeric():
                    valid = True
                else:
                    return jsonify(Error="Phone number does not meet our standards."), 400
            else:
                return jsonify(Error="Incorrect arguments."), 400
        except:
            return jsonify(Error="Incorrect arguments."), 400

        return f(*args, **kwargs)

    return decorated
