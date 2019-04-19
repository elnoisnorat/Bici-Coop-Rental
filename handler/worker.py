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
        try:
            uID = uHandler.insert(form, "Worker")
        except Exception as e:
            raise e
        wDao = WorkerDAO()
        wID = wDao.getWorkerByUID(uID)
        return jsonify("Worker #: " + str(wID) + " was successfully added.")

    def updateStatus(self, form):
        wDao = WorkerDAO()

        wid = form['Worker ID']
        status = form['Status']

        if not wid:                                                                 #Check for null value
            return jsonify(Error="No worker id given")

        if not wDao.getWorkerByID(wid):
            return jsonify(Error="Worker not found."), 404                          #Check if worker exists
        else:
            if status:
                wDao.updateStatus(wid, status)                                      #Update Status
            else:
                return jsonify(Error="No attribute in update request"), 400
            row = wDao.getWorkerByID(wid)
            result = self.build_worker_dict(row)
            return jsonify(Worker=result), 200

    def workerLogin(self, form):
        uHand = UsersHandler()
        email = form['Email']
        password = form['password']

        if email and password:                                                      #No null arguments
            confirmation = uHand.getConfirmation(email)
            if confirmation is False:
                return -4                                                             #User has not confirmed account
            elif confirmation is None:
                return -2
            elif confirmation is True:
                attempts = uHand.getLoginAttempts(email)                                #Get current number of attempts
                blockTime = uHand.getBlockTime(email)                                   #Get current account block time

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

                    # token = jwt.encode(
                    #     {'Role': 'Worker', 'wID': wID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                    #     SECRET_KEY)
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




