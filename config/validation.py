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
            return jsonify(Error="This bicycle is decommissioned")
        return f(*args, **kwargs)
    return decorated

def validPassword(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        password = request.json['password']
        if password:
            passSize = len(password)
            if 8 <= passSize <= 60 \
                    and any(a.islower() for a in password) \
                    and any(a.isupper() for a in password) \
                    and any(a.isnumeric() for a in password):
                    pass
            else:
                return jsonify(Error="Password does not meet our standards."), 400
        else:
            return jsonify(Error="A required field has been left empty."), 400
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
            if oldPassword is None:
                return jsonify(Error="A required field has been left empty."), 400

            if not uHand.checkCurrentPassword(email, oldPassword):
                return jsonify(Error="Invalid credentials."), 400

            newPassword = request.json['newPassword']
            confirmPassword = request.json['confirmPassword']
            if newPassword is None or confirmPassword is None:
                return jsonify(Error="A required field has been left empty."), 400

            if oldPassword != newPassword:
                if newPassword == confirmPassword:
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
                    return jsonify(Error="New password does not match the password confirmation."), 400

            else:
                return jsonify(Error="Please provide a different password."), 400
        except:
            return jsonify(Error="An error has occurred. Please verify submitted data."), 400

        return f(*args, **kwargs)

    return decorated

def validPhoneNumber(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        pnumber = request.json['PNumber']
        if pnumber:
            pnumberSize = len(pnumber)
            if pnumberSize == 10 and pnumber.isnumeric():
                pass
            else:
                return jsonify(Error="Phone number does not meet our standards."), 400
        else:
            return jsonify(Error="A required field has been left empty."), 400
        return f(*args, **kwargs)
    return decorated

def validUpdatePhoneNumber(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            oldPNumber = current_user.pNumber
            newPNumber = request.json['PNumber']

            if newPNumber is None:
                return jsonify(Error="A required field has been left empty."), 400

            if oldPNumber != newPNumber:
                size = len(newPNumber)
                if 10 <= size <= 12 and newPNumber.isnumeric():
                    valid = True
                else:
                    return jsonify(Error="Phone number does not meet our standards."), 400
            else:
                return jsonify(Error="Please choose a different phone number."), 400
        except:
            return jsonify(Error="An error has occurred. Please verify submitted data."), 400

        return f(*args, **kwargs)

    return decorated

def validEmail(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            email = request.json['Email']

            if email is None:
                return jsonify(Error="A required field has been left empty."), 400

            emailSize = len(email)
            if 6 <= emailSize <= 100 and re.match(r"[a-zA-Z0-9_.%+-]+@(?:[a-zA-Z0-9]+\.)+[a-zA-Z]{2,4}", email):
                pass
            else:
                return jsonify(Error="Email does not meet our standards."), 400
        except:
            return jsonify(Error="Incorrect data."), 400
        return f(*args, **kwargs)
    return decorated

def validUpdateNames(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            fName = request.json['FName']
            lName = request.json['LName']
            if fName and lName:
                nameSize = len(fName)
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
            else:
                return jsonify(Error="A required field has been left empty."), 400
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
        return f(*args, **kwargs)
    return decorated

def validUpdateName(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            fName = request.json['FName']
            if fName:
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
            else:
                return jsonify(Error="A required field has been left empty."), 400

        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
        return f(*args, **kwargs)

    return decorated

def validUpdateLName(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            lName = request.json['LName']
            if lName:
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
            else:
                return jsonify(Error="A required field has been left empty."), 400
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
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
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

        return f(*args, **kwargs)

    return decorated

def validPlan(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            name = request.json['name']
            amount = request.json['amount']
            nameSize = len(name)
            if 1 <= nameSize <= 15 \
                    and name.isalnum():
                pass
            else:
                return jsonify(Error="Name provided does not meet our standards."), 400

            if 1 <= len(amount) <= 10 and amount.isnumeric():
                pass
            else:
                return jsonify(Error="Amount provided does not meet our standards."), 400

        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

        return f(*args, **kwargs)

    return decorated

def validBicycle(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            lp = request.json["lp"]
            rfid = request.json["rfid"]
            model = request.json["model"]
            brand = request.json["brand"]
            snumber = request.json["snumber"]

            if lp and rfid and model and brand and snumber:

                if len(lp) <= 10 and lp.isalnum():
                    pass
                else:
                    return jsonify(Error="The license plate provided does not meet our standards."), 400

                if model.isalnum() and len(model) <= 15:
                    pass
                else:
                    return jsonify(Error="The model provided does not meet our standards."), 400
                if len(snumber) <= 12 and snumber.isalnum():
                    pass
                else:
                    return jsonify(Error="The serial number provided does not meet our standards."), 400

                if len(rfid) <= 18 and rfid.isalnum():
                    pass
                else:
                    return jsonify(Error="The rfid provided does not meet our standards."), 400

                if  len(brand) <= 15 and brand.isalnum():
                    pass
                else:
                    return jsonify(Error="The brand provided does not meet our standards."), 400
            else:
                return jsonify(Error="One or more input boxes are empty."), 400
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

        return f(*args, **kwargs)
    return decorated

def validProvide(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        try:
            notes = request.json['Notes']
            email = request.json['Email']
            mID = request.json['mID']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

        try:
            rfid = request.json['rfid']
            if rfid:
                if len(rfid) <= 18 and rfid.isalnum():
                     pass
                else:
                    return jsonify(Error="The rfid provided does not meet our standards."), 400
        except Exception as e:
            pass

        try:
            lp = request.json['lp']
            if lp:
                if len(lp) <= 10 and lp.isalnum():
                    pass
                else:
                    return jsonify(Error="The license plate provided does not meet our standards."), 400
        except Exception as e:
            pass

        if 6 <= len(email) <= 100 and re.match(r"[a-zA-Z0-9_.%+-]+@(?:[a-zA-Z0-9]+\.)+[a-zA-Z]{2,4}", email):
            pass
        else:
            return jsonify(Error="The email provided does not meet our standards."), 400

        if len(mID) <= 10 and mID.isnumeric():
            pass
        else:
            return jsonify(Error="The maintenance identifier does not meet our standards."), 400

        if notes:
            if 0 <= len(notes) <= 180:
                pass
            else:
                return jsonify(Error="The notes provided are too long."), 400
        else:
            pass
        return f(*args, **kwargs)
    return decorated

def validBicycleUpdate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        valid = False
        try:
            lp = request.json["lp"]
            if lp:
                if len(lp) <= 10 and lp.isalnum():
                    valid = True
                    pass
                else:
                    return jsonify(Error="The license plate provided does not meet our standards."), 400
        except Exception as e:
            pass
        try:
            rfid = request.json["rfid"]
            if rfid:
                if len(rfid) <= 18 and rfid.isalnum():
                    valid = True
                    pass
                else:
                    return jsonify(Error="The rfid provided does not meet our standards."), 400
        except Exception as e:
            pass
        try:
            model = request.json["model"]
            if model:
                if len(model) <= 15 and model.isalnum():
                    valid = True
                    pass
                else:
                    return jsonify(Error="The model provided does not meet our standards."), 400
        except Exception as e:
            pass
        try:
            brand = request.json["brand"]
            if brand:
                if len(brand) <= 15 and brand.isalnum():
                    valid = True
                    pass
                else:
                    return jsonify(Error="The brand provided does not meet our standards."), 400
        except Exception as e:
            pass
        try:
            snumber = request.json["snumber"]
            if snumber:
                if len(snumber) <= 12 and snumber.isalnum():
                    valid = True
                    pass
                else:
                    return jsonify(Error="The serial number provided does not meet our standards."), 400
        except Exception as e:
            pass
        try:
            bikestatus = request.json['bikestatus']
            if bikestatus:
                if len(bikestatus) <= 15 and bikestatus.isaplha():
                    valid = True
                    pass
                else:
                    return jsonify(Error="The status provided does not meet our standards."), 400
        except Exception as e:
            pass

        if valid is True:
            return f(*args, **kwargs)
        else:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

    return decorated

def validCheckIn(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        valid = False
        try:
            rfid = request.json['rfid']
            if rfid:
                if len(rfid) <= 18 and rfid.isalnum():
                    valid = True
                    pass
                else:
                    return jsonify(Error="The rfid provided does not meet our standards."), 400
        except Exception as e:
            pass

        try:
            lp = request.json['lp']
            if lp:
                if len(lp) <= 10 and lp.isalnum():
                    valid = True
                    pass
            else:
                return jsonify(Error="The license plate provided does not meet our standards."), 400
        except Exception as e:
            pass

        if valid is True:
            return f(*args, **kwargs)
        else:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
    return decorated

def validCheckOut(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            rfid = request.json['rfid']
            rid = request.json['rid']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

        if rfid and rid:
            if len(rfid) <= 18 and rfid.isalnum():
                pass
            else:
                return jsonify(Error="The rfid provided does not meet our standards."), 400

            if len(rid) <= 10 and rid.isnumeric():
                pass
            else:
                return jsonify(Error="The confirmation code provided does not meet our standards."), 400
        else:
            return jsonify(Error="Missing request inputs."), 400

        return f(*args, **kwargs)
    return decorated

def validSwap(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            rID = request.json['rID']
            oldRFID = request.json['oldRFID']
            newRFID = request.json['newRFID']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

        if rID and oldRFID and newRFID:
            if len(rID) <=10 and rID.isnumeric():
                pass
            else:
                return jsonify(Error="The confirmation code provided does not meet our standards."), 400

            if len(oldRFID) <= 18 and oldRFID.isalnum():
                pass
            else:
                return jsonify(Error="The rfid provided does not meet our standards."), 400

            if len(newRFID) <= 18 and newRFID.isalnum():
                pass
            else:
                return jsonify(Error="The new rfid provided does not meet our standards."), 400
        else:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

        return f(*args, **kwargs)
    return decorated

def validRFID(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            rfid = request.json['rfid']
            if rfid:
                if len(rfid) <= 18 and rfid.isalnum():
                    pass
                else:
                    return jsonify(Error="The rfid provided does not meet our standards."), 400
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
        return f(*args, **kwargs)
    return decorated

def validRID(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            rid = request.json['rid']
            if rid:
                if len(rid) <= 10 and rid.isnumeric():
                    pass
                else:
                    return jsonify(Error="The confirmation code provided does not meet our standards."), 400
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

        return f(*args, **kwargs)
    return decorated

def validWID(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            wID = request.json['wID']
            if wID:
                if len(wID) <= 10 and wID.isnumeric():
                    pass
                else:
                    return jsonify(Error="Incorrect input."), 400
            else:
                return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
        except Exception as e:
            return jsonify("An error has occurred. Please verify the submitted data."), 400
        return f(*args, **kwargs)
    return decorated

def validRentBicycle(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            amount = request.json['amount']
            payment = request.json['payment']
            plan = request.json['plan']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

        if amount and payment and plan:
            if len(amount) == 1 and amount.isnumeric():
                if 1 <= int(amount) <= 4:
                    pass
                else:
                    return jsonify(Error="The amount provided exceeds our allowed limit."), 400
            else:
                return jsonify(Error="The amount provided is not a number."), 400


            if len(payment) == 4 and payment.isupper():
                pass
            else:
                return jsonify(Error="The payment method provided does not meet our standards."), 400

            if 1 <= len(plan) <= 10 and plan.isnumeric():
                pass
            else:
                return jsonify(Error="The selected plan does not meet our standards."), 400
        else:
            return jsonify(Error="A required field has been left empty."), 400
        return f(*args, **kwargs)
    return decorated

def validRentalMaintenance(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role == "Client":
            try:
                lp = request.json['lp']
                if lp:
                    if len(lp) <= 10 and lp.isalnum():
                        pass
                    else:
                        return jsonify(Error="The license plate provided does not meet our standards."), 400
                else:
                    return jsonify(Error="Missing input data."), 400
            except Exception as e:
                return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
        elif current_user.role == "Worker":
            try:
                rfid = request.json['rfid']
                if rfid:
                    if len(rfid) <= 18 and rfid.isalnum():
                        pass
                    else:
                        return jsonify(Error="The rfid provided does not meet our standards."), 400
                else:
                    return jsonify(Error="Missing input data."), 400
            except:
                return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
        else:
            return jsonify(Error="Unauthorized access."), 403
        try:
            services = request.json['Services']
            other = request.json['Other']
            if len(services) > 0 or other:
                pass
            else:
                return jsonify(Error="A required field has been left empty."), 400
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
        return f(*args, **kwargs)
    return decorated
