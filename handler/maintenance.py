import jwt
from flask import jsonify
from flask_login import current_user

from config.encryption import SECRET_KEY
from dao.maintenance import MaintenanceDAO
from handler.bicycle import BicycleHandler
from handler.client import ClientHandler
from handler.rental import RentalHandler
from handler.user import UsersHandler
from handler.worker import WorkerHandler


class MaintenanceHandler:
    def build_maintenance_dict(self, row):
        result = {}
        result['Maintenance ID'] = row[0]
        result['Start Time'] = row[1]
        result['Status'] = row[3]
        result['Notes'] = row[4]
        result['Bicycle ID'] = row[5]
        result['Service'] = row[8]
        return result

    def build_getMaintenance_dict(self, row):
        result = {}
        result['Maintenance ID'] = row[0]
        result['Start Time'] = row[1]
        result['Status'] = row[2]
        result['Bicycle ID'] = row[3]
        result['Plate'] = row[4]
        result['Bicycle Status'] = row[5]
        return result

    def requestMaintenance(self, form):
        mDao = MaintenanceDAO()
        uHand = UsersHandler()
        rHand = RentalHandler()

        if current_user.role == 'Client':
            cid = current_user.roleID
            try:
                plate = form['lp']
            except:
                return jsonify(Error='No plate given.')
            uid = uHand.getUserWithCID(cid)
            bid = rHand.getBIDByCIDAndPlate(cid, plate)
            if not bid:
                return jsonify("You have no current rental with the bicycle provided.")


        elif current_user.role == 'Worker':
            bHand = BicycleHandler()
            wid = current_user.roleID
            rfid = form['rfid']
            uid = uHand.getUserIDByEmail(current_user.email)
            bid = bHand.getBIDByRFID(rfid)
            if not bid:
                return jsonify("The bicycle is not registered in the inventory.")
        print(bid)
        noRep = mDao.getRequestByBID(bid)

        if noRep:
            return jsonify(Error="Bicycle already has a maintenance request.")
        try:
            mID = mDao.requestMaintenance(uid, bid)                                  #Insert #1
        except Exception as e:
            raise e

        return jsonify("Maintenance request #" + str(mID) + " has been created.")


    def getMaintenance(self, form):
        mDao = MaintenanceDAO()
        row = mDao.getMaintenance()
        if not row:
            return jsonify("There are no current maintenance requests.")

        result_list = []
        for row in row:
            result = self.build_getMaintenance_dict(row)
            result_list.append(result)
        return jsonify(Details=result)

    def provideMaintenance(self, form):
        notes = form['Notes']
        wid = form['wID']
        mid = form['mID']
        service = form['service']
        if wid:
            mDao = MaintenanceDAO()
            wHand = WorkerHandler()
            cHand = ClientHandler()
            reqID = mDao.getRequestedByWithMID(mid)
            if wHand.getWorkerByUID(reqID):
                role = 'Worker'
            elif cHand.getCIDByUID(reqID):
                role = 'Client'
                uHand = UsersHandler()
                pNumber = uHand.getPhoneNumberByUID(reqID)
            else:
                return jsonify(Error="Invalid maintenance request.")

            try:
                    mDao.provideMaintenance(wid, mid, notes, service, role)
            except Exception as e:
                raise e

            row = mDao.getRequestByMID(mid)
            if not row:
                return jsonify("No maintenance with those parameters.")

            result = self.build_maintenance_dict(row)
            if role == 'Worker':
                return jsonify(Maintenance=result)
            elif role == 'Client':
                cResult = {
                    "ALERT": "Please call the user at " + str(pNumber),
                    "Maintenance": result
                }
                return jsonify(cResult)
            else:
                return jsonify(Error="Invalid maintenance request.")
        else:
            return jsonify(Error="No worker id provided.")
