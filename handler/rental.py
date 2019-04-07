import jwt
from flask import jsonify

from config.encryption import SECRET_KEY
from dao.rental import RentalDAO
from handler.bicycle import BicycleHandler
from handler.client import ClientHandler
from handler.user import UsersHandler


class RentalHandler:
    def build_checkIn_dict(self, row):
        result = {}
        result['Rental ID'] = row[0]
        result['Start Time'] = row[1]
        result['End Time'] = row[2]
        result['Client ID'] = row[4]
        result['Dispatched By'] = row[5]
        result['Received By'] = row[6]
        result['Bicycle ID'] = row[7]
        result['Transaction ID'] = row[8]
        return result

    def build_rental_dict(self,row):
        result = {}
        result['rentalID'] = row[0]
        result['Rental Start Date'] = row[1]
        result['Date Delivered'] = row[2]
        result['Due Date'] = row[7]
        result['BID'] = row[6]
        return result



    def rentBicycle(self, cid, tid):
        rDao = RentalDAO()
        return rDao.rentBicycle(cid, tid)

    def getRentalByCID(self, form):
        token = form['token']

        cHandler = ClientHandler()
        rDao = RentalDAO()

        try:
            data = jwt.decode(token, SECRET_KEY)
            cID = data['cID']
        except:
            return jsonify(Error="Invalid token.")

        if not cHandler.getClientByCID(cID):
               return jsonify(Error="Client does not exist."), 401

        rental_list = rDao.getRentalByCID(cID)
        result_list = []
        for row in rental_list:
            result = self.build_rental_dict(row)
            result_list.append(result)
        if len(rental_list) == 0:
            return jsonify("You have no current rental at this moment.")
        return jsonify(CurrentRentals=result_list)

    def getBIDByCID(self, cid):
        rDao = RentalDAO()
        bid = rDao.getBIDByCID(cid)
        return bid

    def checkInBicycle(self, form):
        rfid = form['rfid']
        plate = form['lp']
        token = form['token']
        bHand = BicycleHandler()
        rDao = RentalDAO()

        if not rfid:
            if not plate:
                return jsonify(Error="Bicycle was not scanned.")
            else:
                bid = bHand.getBIDByPlate(plate)

        else:

            try:
                data = jwt.decode(token, SECRET_KEY)
                wID = data['wID']
            except:
                return jsonify("Invalid token at check in")

            bid = bHand.getBIDByRFID(rfid)

        if not bid:
            return jsonify(Error="Bicycle does not exist.")
        rid = rDao.getRIDByBID(bid)
        if not rid:
            return jsonify(Error="Rental does not exist.")

        rDao.checkIn(wID, rid)

        row = rDao.getRentalByID(rid)
        rental = self.build_checkIn_dict(row)
        return jsonify(Rental=rental)

    def checkOutBicycle(self, form):
        rid = form['rid']
        email = form['email']
        rfid = form['rfid']
        token = form['token']

        if not rfid:
            return jsonify(Error="Bicycle was not scanned.")

        try:
            data = jwt.decode(token, SECRET_KEY)
            wID = data['wID']
        except:
            return jsonify("Invalid token at check out")

        rDao = RentalDAO()
        bHand = BicycleHandler()
        bid = bHand.getBIDByRFID(rfid)
        if not bid:
            return jsonify(Error="Bicycle does not exist.")

        if not rid:
            if email:
                uHand = UsersHandler()
                cHand = ClientHandler()
                uID = uHand.getUserIDByEmail(email)
                cID = cHand.getClientByUID(uID)
                rid = rDao.getRentalByCID(cID)
            else:
                return jsonify(Error="No valid method to identify ")

        if not rid:
            return jsonify(Error="Rental does not exist.")

        bStatus = bHand.getStatusByID(bid)
        if bStatus == 'Available':
            bHand.updateStatusIsAvailable(bid)
        elif bStatus == 'Reserved':
            bHand.updateStatusIsReserved(bid)

        else:
            print('ROLLBACK')
            #RollBack

        rDao.checkOut(wID, bid, rid)

        row = rDao.getRentalByID(rid)
        if not row:
            #RollBack
            return jsonify(Error="Rental was not created correctly.")
        rental = self.build_checkIn_dict(row)
        return jsonify(Rental=rental)





