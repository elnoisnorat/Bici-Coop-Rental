from flask import request, jsonify
from functools import wraps
from flask_login import current_user
from dao.bicycle import BicycleDAO
from handler.user import UsersHandler
import re


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
        passSize = len(password)
        if 8 <= passSize <= 60 \
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
            password_list = []
            oldPassword = request.json['oldPassword']
            if not uHand.checkCurrentPassword(email, oldPassword):
                return jsonify(Error="Incorrect arguments."), 400 #############################

            newPassword = request.json['newPassword']
            confirmPassword = request.json['confirmPassword']
            if newPassword is None or confirmPassword is None:
                return jsonify(Error="Incorrect arguments."), 400

            if oldPassword != newPassword and newPassword == confirmPassword:
                password_list.append(oldPassword)
                password_list.append(newPassword)
                for password in password_list:
                    size = len(password)
                    if 8 <= size <= 60 \
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
        pnumberSize = len(pnumber)
        if pnumberSize == 10 and pnumber.isnumeric():
            pass
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

            if newPNumber is None:
                return jsonify(Error="Incorrect arguments."), 400

            if oldPNumber != newPNumber:
                size = len(newPNumber)
                if 10 <= size <= 12 and newPNumber.isnumeric():
                    valid = True
                else:
                    return jsonify(Error="Phone number does not meet our standards."), 400
            else:
                return jsonify(Error="Incorrect arguments."), 400
        except:
            return jsonify(Error="Incorrect arguments."), 400

        return f(*args, **kwargs)

    return decorated

def validEmail(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            email = request.json['Email']

            if email is None:
                return jsonify(Error="Incorrect arguments."), 400

                emailSize = len(email)
                if 6 <= size <= 100 and re.match(r"[a-zA-Z0-9_.%+-]+@(?:[a-zA-Z0-9]+\.)+[a-zA-Z]{2,4}", email):
                    pass
                else:
                    return jsonify(Error="Phone number does not meet our standards."), 400
            else:
                return jsonify(Error="Incorrect arguments."), 400
        except:
            return jsonify(Error="Incorrect arguments."), 400

        return f(*args, **kwargs)

    return decorated

def validUpdateNames(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            fName = request.json['FName']
            nameSize = len(fName)
            lName = request.json['LName']
            lNameSize = len(lName)

            if 1 <= nameSize <= 50 \
                    and all(x.isalpha()
                            or x.isspace()
                            or x == '-'
                            for x in fName) \
                    and not fName.isspace() \
                    and fName.find('  ') == -1 \
                    and fName.find('--') == -1 \
                    and fName.find('- ') == -1 \
                    and fName.find(' -') == -1:
                pass
            else:
                return jsonify(Error="Name provided does not meet our standards."), 400

            if 1 <= lNameSize <= 50 \
                    and all(x.isalpha()
                            or x.isspace()
                            or x == '-'
                            for x in lName) \
                    and not lName.isspace() \
                    and lName.find('  ') == -1 \
                    and lName.find('--') == -1 \
                    and lName.find('- ') == -1 \
                    and lName.find(' -') == -1:
                pass
            else:
                return jsonify(Error="Last name provided does not meet our standards."), 400
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        return f(*args, **kwargs)

    return decorated

def validUpdateName(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            fName = request.json['FName']
            nameSize = len(fName)

            if 1 <= nameSize <= 50 \
                    and all(x.isalpha()
                            or x.isspace()
                            or x == '-'
                            for x in fName) \
                    and not fName.isspace() \
                    and fName.find('  ') == -1 \
                    and fName.find('--') == -1 \
                    and fName.find('- ') == -1 \
                    and fName.find(' -') == -1:
                pass
            else:
                return jsonify(Error="Name provided does not meet our standards."), 400
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
        return f(*args, **kwargs)

    return decorated

def validUpdateLName(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            lName = request.json['LName']
            lNameSize = len(lName)

            if 1 <= lNameSize <= 50 \
                    and all(x.isalpha()
                            or x.isspace()
                            or x == '-'
                            for x in lName) \
                    and not lName.isspace() \
                    and lName.find('  ') == -1 \
                    and lName.find('--') == -1 \
                    and lName.find('- ') == -1 \
                    and lName.find(' -') == -1:
                pass
            else:
                return jsonify(Error="Last name provided does not meet our standards."), 400
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
        return f(*args, **kwargs)

    return decorated

def validUserCreation(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            fName = request.json['FName']
            lName = request.json['LName']
            email = request.json['Email']
            password = request.json['password']
            pnumber = request.json['PNumber']
            nameSize = len(fName)
            lNameSize = len(lName)
            emailSize = len(email)
            passSize = len(password)
            pnumberSize = len(pnumber)

            if 1 <= nameSize <= 50 \
                    and all(x.isalpha()
                            or x.isspace()
                            or x == '-'
                            for x in fName) \
                    and not fName.isspace() \
                    and fName.find('  ') == -1 \
                    and fName.find('--') == -1 \
                    and fName.find('- ') == -1 \
                    and fName.find(' -') == -1:
                pass
            else:
                return jsonify(Error="Name provided does not meet our standards."), 400

            if 1 <= lNameSize <= 50 \
                    and all(x.isalpha()
                            or x.isspace()
                            or x == '-'
                            for x in lName) \
                    and not lName.isspace() \
                    and lName.find('  ') == -1 \
                    and lName.find('--') == -1 \
                    and lName.find('- ') == -1 \
                    and lName.find(' -') == -1:
                pass
            else:
                return jsonify(Error="Last name provided does not meet our standards."), 400

            if 8 <= passSize <= 60 \
                    and any(a.islower() for a in password) \
                    and any(a.isupper() for a in password) \
                    and any(a.isnumeric() for a in password):
                pass
            else:
                return jsonify(Error="Password provided does not meet our standards."), 400

            if 6 <= emailSize <= 100 and re.match(r"[a-zA-Z0-9_.%+-]+@(?:[a-zA-Z0-9]+\.)+[a-zA-Z]{2,4}", email):
                pass
            else:
                return jsonify(Error="Email provided does not meet our standards."), 400

            if pnumberSize == 10 and pnumber.isnumeric():
                pass
            else:
                return jsonify(Error="Phone number does not meet our standards."), 400


        except:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        return f(*args, **kwargs)

    return decorated