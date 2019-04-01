import jwt
from flask import jsonify

from config.encryption import SECRET_KEY
from dao.maintenance import MaintenanceDAO
from handler.bicycle import BicycleHandler
from handler.rental import RentalHandler
from handler.user import UsersHandler


class MaintenanceHandler:
    def requestMaintenance(self, form):
        mDao = MaintenanceDAO()
        uHand = UsersHandler()
        rHand = RentalHandler()
        token = form['token']
        notes = form['notes']

        try:
            data = jwt.decode(token, SECRET_KEY)

        except:
            return jsonify(Error="Invalid token in request maintenance")

        if data['Role'] == 'Client':
            cid = data['cID']
            uid = uHand.getUserWithCID(cid)
            bid = rHand.getBIDByCID(cid)
            if not bid:
                return jsonify("You have no current rental at the moment.")

        elif data['Role'] == 'Worker':
            bHand = BicycleHandler()
            wid = data['wID']
            rfid = form['RFID']
            uid = uHand.getUserWithWID(wid)
            bid = bHand.getBIDByRFID(rfid)
            if not bid:
                return jsonify("The bicycle is not registered in the inventory.")

        rID = mDao.requestMaintenance(uid, bid, notes)
        return jsonify("Maintenance request: " + rID + " has been created.")




        '''
        MID SERIAL PRIMARY KEY,
        StartTime TIMESTAMP,
        EndTime TIMESTAMP,
        Status varchar(15),
        Notes VARCHAR(180),
        Bike INTEGER REFERENCES Bike(BID),
        RequestedBy INTEGER REFERENCES Worker(WID),
        ServicedBy INTEGER REFERENCES Worker(WID)
        '''