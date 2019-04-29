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
    def __init__(self):
        self.valid_services = ["Clean Up", "Pedal Adjustment", "New Plate", "Tune Up", "Transmission Adjustment", "Flat Tire", "New Tire", "Break Adjustment", "New Break", "Maneuver Adjustment", "New RFID Tag"]

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
        result['Service'] = row[6]
        result['Brand'] = row[7]
        result['Model'] = row[8]
        return result

    def requestMaintenance(self, form):
        mDao = MaintenanceDAO()
        uHand = UsersHandler()
        rHand = RentalHandler()

        uid = uHand.getUserIDByEmail(current_user.email)

        if current_user.role == 'Client':
            cid = current_user.roleID
            try:
                plate = form['lp']
            except:
                return jsonify(Error='An error has occurred. Please verify the submitted arguments.'), 400
            bid = rHand.getBIDByCIDAndPlate(cid, plate)
            if not bid:
                return jsonify("You have no current bicycle rental at this time.") #Pending

        elif current_user.role == 'Worker':
            bHand = BicycleHandler()
            try:
                rfid = form['rfid']
            except Exception as e:
                return jsonify("An error has occurred. Please verify the submitted arguments."), 400
            if rfid:
                bid = bHand.getBIDByRFIDForMaintenance(rfid)
            else:
                bid = None

            if not bid:
                try:
                    plate = form['lp']
                except Exception as e:
                    return jsonify("An error has occurred. Please verify the submitted arguments."), 400
                if plate:
                    bid = bHand.getBIDByPlateForMaintenance(plate)
                else:
                    bid = None
                if not bid:
                    return jsonify("An error has occurred. Please verify the submitted arguments."), 400
        try:
            service_list = form["Services"]
            filteredArgs = []
            active_service_list = mDao.getRequestByBID(bid)
            print(active_service_list)
            for service in service_list:  # Filter arguments received using a dictionary
                if service and service in self.valid_services and service not in active_service_list:
                    filteredArgs.append(service)
        except Exception as e:
            return jsonify(Error="An error has occurred."), 400

        try:
            other = form['Other']
            if other and other not in active_service_list:
                filteredArgs.append(other)
        except Exception as e:
            pass

        if len(filteredArgs) == 0:
            return jsonify(Error="These services have already been requested."), 400

        try:
            mDao.requestMaintenance(uid, bid, filteredArgs)  # Insert #1
            return jsonify("Maintenance request was successfully created.")
        except Exception as e:
            return jsonify("An error has occurred."), 400

    def getMaintenance(self, form):
        mDao = MaintenanceDAO()
        maintenance_list = mDao.getMaintenance()
        if not maintenance_list:
            return jsonify("There are no maintenance requests at this time.")

        result_list = []
        for row in maintenance_list:
            result = self.build_getMaintenance_dict(row)
            result_list.append(result)
        return jsonify(Details=result_list)

    def provideMaintenance(self, form):
        try:
            notes = form['Notes']
            email = form['Email']
            mid = form['mID']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
        wHand = WorkerHandler()
        if email is None:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        wid = wHand.getWIDByEmail(email)
        if wid and mid:
            mDao = MaintenanceDAO()
            wHand = WorkerHandler()
            cHand = ClientHandler()
            reqID = mDao.getRequestedByWithMID(mid)
            if reqID is None:
                return jsonify(Error="An error has occurred."), 400

            if wHand.getWorkerByUID(reqID):
                role = 'Worker'
            elif cHand.getCIDByUID(reqID):
                role = 'Client'
                uHand = UsersHandler()
                pNumber = uHand.getPhoneNumberByUID(reqID)
            else:
                return jsonify(Error="Unauthorized access."), 403

            mService = mDao.getService(mid)

            try:
                if mService == "New Plate":
                    plate = form['lp']
                    if plate is None:
                        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
                    check = mDao.provideMaintenancePlate(wid, mid, notes, role, plate)
                elif mService == "New RFID Tag":
                    rfid = form['rfid']
                    if rfid is None:
                        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
                    check = mDao.provideMaintenanceRFID(wid, mid, notes, role, rfid)
                else:
                    check = mDao.provideMaintenance(wid, mid, notes, role)

            except Exception as e:
                return jsonify(Error="An error has occurred."), 400

            if check is None:
                return jsonify(Error="An error has occurred."), 403
            elif check > 0:
                return jsonify("Maintenance has been completed.")
            elif check == 0:
                if role == 'Worker':
                    return jsonify("Maintenance has been completed.")
                elif role == 'Client':
                    cResult = {
                        "ALERT": "Please call the user at " + str(pNumber),
                        "Maintenance": "Maintenance has been completed."
                    }
                    return jsonify(cResult)
        else:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
