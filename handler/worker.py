from flask import jsonify
from config.encryption import SECRET_KEY, ENC_ALG
from flask_login import current_user

from handler.punchCard import PunchCardHandler
from handler.user import UsersHandler
from dao.user import UsersDAO
from dao.worker import WorkerDAO
import jwt
import datetime


class WorkerHandler:

    def __init__(self):
        self.worker_attributes = ['fName', 'lName', 'pNumber', 'email' 'wid', 'uid', 'status', 'orderby']
        self.orderBy_attributes = ['fName', 'lName', 'pNumber', 'wid', 'uid', 'status']

    def build_worker_dict(self, row):
        result = {}
        result['Worker ID'] = row[0]
        result['First Name'] = row[1]
        result['Last Name'] = row[2]
        result['Email'] = row[3]
        result['Phone Number'] = row[4]
        result['Status'] = row[5]
        return result

    def getWorker(self, form):
        wDao = WorkerDAO()

        filteredArgs = {}
        for arg in form:
            if form[arg] and arg in self.worker_attributes:
                if arg != 'orderby':
                    filteredArgs[arg] = form[arg]
                elif form[arg] in self.orderBy_attributes:
                    filteredArgs[arg] = form[arg]

        if len(filteredArgs) == 0:
            worker_list = wDao.getAllWorkers()

        elif not 'orderby' in filteredArgs:
            worker_list = wDao.getWorkerByArguments(filteredArgs)

        elif ((len(filteredArgs)) == 1) and 'orderby' in filteredArgs:
            worker_list = wDao.getWorkerWithSorting(filteredArgs['orderedby'])

        else:
            worker_list = wDao.getWorkerByArgumentsWithSorting(filteredArgs)

        result_list = []

        for row in worker_list:
            result = self.build_worker_dict(row)
            result_list.append(result)

        return jsonify(Inventory=result_list)

    def insert(self, form):
        uHandler = UsersHandler()
        if uHandler.getUserIDByEmail(form['Email']) is not None:
            return jsonify(Error="Please use another email address."), 400
        try:
            uHandler.insert(form, "Worker")
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400
        return jsonify("Account was successfully created.")

    def updateStatus(self, form):
        try:
            wid = form['wID']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted data."), 400

        wDao = WorkerDAO()
        if not wid:                                                                 #Check for null value
            return jsonify(Error="A required field has been left empty."), 400

        worker = wDao.getWorkerByID(wid)

        if worker is None:
            return jsonify(Error="Invalid credentials."), 400
        else:
            status = worker[5]
            if status == 'ACTIVE':
                wDao.updateStatus(wid, 'INACTIVE')                                      #Update Status

            elif status == 'ACTIVE':
                wDao.updateStatus(wid, 'ACTIVE')                                      #Update Status

            else:
                return jsonify(Error="Invalid credentials."), 400

            # row = wDao.getWorkerByID(wid)
            # result = self.build_worker_dict(row)
            # return jsonify(Worker=result)
            return jsonify("Update was successful.")

    def workerLogin(self, form):
        uHand = UsersHandler()
        email = form['Email']
        password = form['password']
        print(email)
        print(password)
        if email and password:                                                      #No null data
            confirmation = uHand.getConfirmation(email)
            if confirmation is False or confirmation is None:
                return -2
            elif confirmation is True:
                attempts = uHand.getLoginAttempts(email)                                #Get current number of attempts
                blockTime = uHand.getBlockTime(email)                                   #Get current account block time

                print(datetime.datetime.now())
                print(blockTime)

                if datetime.datetime.now() > blockTime:                                 #If current time > block time proceed

                    if attempts == 7:
                        uHand.setBlockTime(email)                                       #Lock account at 7 attempts
                        return -1

                    wDao = WorkerDAO()
                    worker = wDao.workerLogin(email, password)                          #Validate User
                    if worker is None:
                        uHand.addToLoginAttempt(email)                                  #Add to login attempt
                        return -2
                    elif worker[1] == "INACTIVE":                                       #Reject if inactive
                        return -3

                    uHand.resetLoginAttempt(email)                                      #Set login attempt to 0

                    userInfo = uHand.getProfile(email)                                  #Get User information

                    response = {
                        'info' : userInfo
                    }

                    pHand = PunchCardHandler()
                    pHand.inType(worker[0])                                             #Make Punch Card Entry
                    return jsonify(response)
                else:
                    return -1
        else:
            return -2

    def workerLogOut(self):
        wid = current_user.roleID
        pHand = PunchCardHandler()
        pHand.outType(wid)                                                          #Make Punch Card Entry

    def getWorkerByUID(self, reqID):
        wDao = WorkerDAO()
        result = wDao.getWorkerByUID(reqID)
        return result

    def getWIDByEmail(self, email):
        wDao = WorkerDAO()
        result = wDao.getWIDByEmail(email)
        return result

    def getWorkerForMaintenance(self, email):
        wDao = WorkerDAO()
        result = wDao.getWorkerForMaintenance(email)
        return result

    def getConfirmedWorker(self):
        wDao = WorkerDAO()
        worker_list = wDao.getConfirmedWorker()
        result_list = []
        for row in worker_list:
            result = self.build_worker_dict(row)
            result_list.append(result)
        return jsonify(result_list)




