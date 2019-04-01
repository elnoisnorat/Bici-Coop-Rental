from flask import jsonify
from config.encryption import SECRET_KEY, ENC_ALG
from handler.user import UsersHandler
from dao.user import UsersDAO
from dao.worker import WorkerDAO
import jwt
import datetime


class WorkerHandler:

    def __init__(self):
        self.worker_attributes = ['wid', 'uid', 'status', 'orderby']

    def build_worker_dict(self, row):
        result = {}
        result['wid'] = row[0]
        result['fName'] = row[1]
        result['lName'] = row[2]
        result['status'] = row[3]
        return result

    def getWorker(self, args):
        wDao = WorkerDAO()
        if not args:
            worker = wDao.getAllWorkers()
        for arg in args:
            if not arg in self.worker_attributes:
                return jsonify(Error="Invalid Argument"), 401

        if not 'orderby' in args:
            worker_list = wDao.getWorkerByArguments(args)

        elif ((len(args)) == 1) and 'orderby' in args:
            worker_list = wDao.getWorkerWithSorting(args.get('orderby'))

        else:
            worker_list = wDao.getWorkerByArgumentsWithSorting(args)

        result_list = []

        for row in worker_list:
            result = self.build_worker_dict(row)
            result_list.append(result)

        return jsonify(Inventory=result_list)

    def insert(self, form):
        email = form['Email']
        status = form['status']

        uHandler = UsersHandler()
        wDao = WorkerDAO()
        uDao = UsersDAO()
        uid = uDao.getUserByEmail(email)
        if not uid:
            uid = uHandler.insert(form)

        if wDao.getWorkerByUID(uid):
            return jsonify(Error="User is already a Worker")
        if uid and status:
            wID = wDao.insert(uid, status)
            return jsonify("Worker #: " + wID + " was successfully added.")
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
