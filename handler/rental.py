import jwt
from flask import jsonify
from flask_login import current_user

from config.encryption import SECRET_KEY
from dao.rental import RentalDAO
from handler.bicycle import BicycleHandler
from handler.client import ClientHandler
from handler.user import UsersHandler
import datetime


class RentalHandler:
    def build_checkIn_dict(self, row):
        result = {}
        result['Rental ID'] = row[0]
        result['Start Time'] = row[1]
        result['End Time'] = row[2]
        result['Client ID'] = row[3]
        result['Bicycle ID'] = row[4]
        result['Dispatched By'] = row[5]
        result['Received By'] = row[6]
        result['Due Date'] = row[7]

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
        #token = form['token']

        cHandler = ClientHandler()
        rDao = RentalDAO()
        cID = current_user.roleID
        '''
        try:
            data = jwt.decode(token, SECRET_KEY)
            cID = data['cID']
        except:
            return jsonify(Error="Invalid token.")
        '''

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
        #token = form['token']
        bHand = BicycleHandler()
        rDao = RentalDAO()
        wID = current_user.roleID
        if not rfid:
            try:
                plate = form['lp']
                bid = bHand.getBIDByPlate(plate)
            except Exception as e:
                return jsonify(Error="Bicycle was not scanned.")
        else:
            bid = bHand.getBIDByRFID(rfid)
        '''
        try:
            data = jwt.decode(token, SECRET_KEY)
            wID = data['wID']
        except:
            return jsonify("Invalid token at check in")
        '''
        if not bid:
            return jsonify(Error="Bicycle does not exist.")
        rid = rDao.getRIDByBID(bid)
        if not rid:
            return jsonify(Error="Rental does not exist.")

        debt = rDao.checkIn(wID, rid)

        row = rDao.getRentalByID(rid)
        rental = self.build_checkIn_dict(row)
        if debt is True:
            result = {
                "ALERT": "User has returned the bicycle after the due date.",
                "Rental": rental
            }
            return jsonify(result)
        else:
            return jsonify(Rental=rental)


    def checkOutBicycle(self, form):
        rid = form['rid']
        rfid = form['rfid']
        #token = form['token']
        wID = current_user.roleID
        if not rfid:
            return jsonify(Error="Bicycle was not scanned.")
        '''
        try:
            data = jwt.decode(token, SECRET_KEY)
            wID = data['wID']
        except:
            return jsonify("Invalid token at check out")
        '''
        rDao = RentalDAO()
        bHand = BicycleHandler()
        bid = bHand.getBIDByRFID(rfid)
        if not bid:
            return jsonify(Error="Bicycle does not exist.")

        if not rid:
            email = form['email']
            if email:
                uHand = UsersHandler()
                cHand = ClientHandler()
                uID = uHand.getUserIDByEmail(email)
                cID = cHand.getClientByUID(uID)
                rid = rDao.getRentalByCIDCheckOut(cID)
            else:
                return jsonify(Error="No valid method to identify ")

        if not rid:
            return jsonify(Error="Rental does not exist.")

        bStatus = bHand.getStatusByID(bid)
        print(bStatus)
        if bStatus == 'AVAILABLE':
            try:
                bHand.updateStatusIsAvailable(bid, wID, rid)
            except Exception as e:
                return jsonify(Error="An error has occurred.")
        elif bStatus == 'RESERVED':
            try:
                bHand.updateStatusIsReserved(bid, wID, rid)
            except Exception as e:
                return jsonify(Error="An error has occurred.")
        else:
            return jsonify(Error="Bicycle is not in a condition to be rented.")

        #rDao.checkOut(wID, bid, rid)

        row = rDao.getRentalByID(rid)
        if not row:
            #RollBack
            return jsonify(Error="Rental was not created correctly.")
        rental = self.build_checkIn_dict(row)
        return jsonify(Rental=rental)

    def getBIDByCIDAndPlate(self, cid, plate):
        rDao = RentalDAO()
        bid = rDao.getBIDByCIDAndPlate(cid, plate)
        return bid

    def getNewRentals(self, tid):
        rDao = RentalDAO()
        rental_list = rDao.getNewRentals(tid)
        return rental_list

    # def swapBicycle(self, form):
    #     rDao = RentalDAO()
    #     try:
    #         rid = form["rID"]
    #         oldRFID = form["oldRFID"]
    #         newRFID = form["newRFID"]
    #     except Exception as e:
    #         return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    #
    #     if rid and oldRFID and newRFID:
    #         rDao = RentalDAO()
    #         bHand = BicycleHandler()
    #
    #         oldBID = rDao.get_rental_by_rid_and_rfid(rid, oldRFID)
    #         if oldBID is None:
    #             return jsonify(Error="This bicycle is not linked to the provided information."), 400
    #
    #         newBID = bHand.getBIDByRFID(newRFID)
    #
    #
    #         if oldBID and newBID:
    #             oldBStatus = bHand.getStatusByID(oldBID)
    #             newBStatus = bHand.getStatusByID(newBID)
    #
    #             if oldBStatus == "MAINTENANCE":
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #             if bStatus == 'AVAILABLE':
    #                 try:
    #                     bHand.swapStatusIsAvailable(oldValid, newValid, rid)
    #                 except Exception as e:
    #                     return jsonify(Error="An error has occurred.")
    #             elif bStatus == 'RESERVED':
    #                 try:
    #                     bHand.swapStatusIsReserved(oldValid, newValid, rid)
    #                 except Exception as e:
    #                     return jsonify(Error="An error has occurred.")
    #             else:
    #                 return jsonify(Error="Bicycle is not in a condition to be rented.")
    #
    #
    #     rental_list = rDao.getNewRentals(tid)
    #     return rental_list
