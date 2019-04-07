from flask import jsonify
from config.encryption import SECRET_KEY, ENC_ALG
from handler.user import UsersHandler
from dao.user import UsersDAO
from dao.worker import WorkerDAO
import jwt
import datetime


class WorkerHandler:

    def __init__(self):
        self.worker_attributes = ['fName', 'lName', 'pNumber', 'wid', 'uid', 'status', 'orderby']
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
        email = form['Email']

        uHandler = UsersHandler()
        wDao = WorkerDAO()
        uDao = UsersDAO()
        uid = uDao.getUserIDByEmail(email)
        if not uid:
            uid = uHandler.insert(form)

        if wDao.getWorkerByUID(uid):
            return jsonify(Error="User is already a Worker")
        if uid:
            wID = wDao.insert(uid)
            return jsonify("Worker #: " + str(wID) + " was successfully added.")
        else:
            return jsonify(Error="Null value in attributes of the worker."), 401

    def updateStatus(self, form):
        wDao = WorkerDAO()

        wid = form['wid']
        status = form['status']

        if not wid:
            return jsonify(Error="No worker id given")

        if not wDao.getWorkerByID(wid):
            return jsonify(Error="Worker not found."), 404
        else:
            if len(form) != 2:
                return jsonify(Error="Malformed update request."), 400
            else:
                if status:
                    wDao.updateStatus(wid, status)
                else:
                    return jsonify(Error="No attributes in update request"), 400

                row = wDao.getWorkerByID(wid)
                result = self.build_worker_dict(row)
                return jsonify(Worker=result), 200

    def workerLogin(self, form):
        print(form)
        email = form['email']
        password = form['password']
        if email and password:
            wDao = WorkerDAO()
            wID = wDao.workerLogin(email, password)
            token = jwt.encode(
                {'Role': 'Worker', 'wID': wID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                SECRET_KEY)
            response = {
                'token': token.decode('UTF-8')
            }
            return jsonify(response)
        else:
            return jsonify(Error="Invalid username or password."), 401
