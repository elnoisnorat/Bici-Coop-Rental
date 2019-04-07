import jwt
from flask import jsonify

from config.encryption import SECRET_KEY
from dao.maintenance import MaintenanceDAO
from dao.serviceMaintenance import ServiceMaintenanceDAO
from handler.user import UsersHandler


class ServiceMaintenanceHandler:
    def requestServiceMaintenance(self, form):
        sDao = ServiceMaintenanceDAO()
        uHand = UsersHandler()
        token = form['token']
        service = form['service']
        price = form['price']
        notes = form['notes']
        try:
            data = jwt.decode(token, SECRET_KEY)
            if data['Role'] == 'Client':
                cid = data['cID']
                userJson = uHand.getUserWithCID(cid)
                uid = userJson['uid']
                uName = userJson['FName']
                uLName = userJson['LName']
        except:
            return jsonify(Error="Invalid token")

        sID = sDao.requestServiceMaintenance(uid, uName, uLName, service, price, notes)
        return jsonify("Personal maintenance request: " + sID + " has been created.")




        '''
            SMID SERIAL PRIMARY KEY, 
            FName varchar(50), 
            LName varchar(50), 
            Bike varchar(50), 
            Service varchar(100), 
            Price REAL, 
            WorkedBy INTEGER REFERENCES Worker(WID), 
            WorkStatus varchar(15), 
            Notes VARCHAR(180), 
            STime TIMESTAMP, 
            ETime TIMESTAMP
        '''