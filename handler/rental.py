import traceback

import jwt
import stripe
from flask import jsonify
from flask_login import current_user
from app import scheduler
from config.encryption import SECRET_KEY
from dao.rental import RentalDAO
from handler.bicycle import BicycleHandler
from handler.client import ClientHandler
from handler.user import UsersHandler
import datetime

hook_key = 'whsec_1BYC3kEVQ2Ssu02IXLeTFiNhq5cdWMF2'



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
        result['Due Date'] = row[3]
        #result['BID'] = row[4]
        result['Debt Status'] = row[5]
        return result



    # def rentBicycle(self, cid, tid):
    #     rDao = RentalDAO()
    #     return rDao.rentBicycle(cid, tid)

    def getRentalByCID(self, form):
        cHandler = ClientHandler()
        rDao = RentalDAO()
        cID = current_user.roleID

        if not cHandler.getClientByCID(cID):
               return jsonify(Error="Unauthorized access."), 403

        rental_list = rDao.getRentalByCID(cID)
        result_list = []
        for row in rental_list:
            result = self.build_rental_dict(row)
            print(result)
            result_list.append(result)
        if len(rental_list) == 0:
            return jsonify("You have no current rental at this moment.")
        return jsonify(CurrentRentals=result_list)

    def getRentalAmountByCID(self, cID):
        cHandler = ClientHandler()
        rDao = RentalDAO()

        if not cHandler.getClientByCID(cID):
               return jsonify(Error="Unauthorized access."), 403

        amount = rDao.getRentalAmountByCID(cID)
        return amount

    def getBIDByCID(self, cid):
        rDao = RentalDAO()
        bid = rDao.getBIDByCID(cid)
        return bid

    def checkInBicycle(self, form):
        try:
            rfid = form['rfid']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        bHand = BicycleHandler()
        rDao = RentalDAO()
        wID = current_user.roleID
        if not rfid:
            try:
                plate = form['lp']
                bid = bHand.getBIDByPlate(plate)
            except Exception as e:
                return jsonify(Error="No arguments given to identify the bicycle."), 400
        else:
            bid = bHand.getBIDByRFID(rfid)

        if not bid:
            return jsonify(Error="A bicycle with the given arguments does not exist. "
                                 "Please verify the submitted arguments."), 400
        rid = rDao.getRIDByBID(bid)
        if not rid:
            return jsonify(Error="There is no current rental for this bicycle."), 400

        debt = rDao.checkIn(wID, rid)
        stripeID = rDao.getStripeToken(rid)
        row = rDao.getRentalByID(rid)
        rental = self.build_checkIn_dict(row)

        if stripeID == 'CASH':
            if debt is True:
                money2get = rDao.getDebtToCollect(rid)
                return jsonify("Check-in was successful, but the user has exceeded their rental period. Please collect $" + money2get + ".")

        else:
            try:
                stripe.Subscription.delete(stripeID)
            except Exception as e:
                return jsonify("Check-in was successful, but there was an error closing the payment subscription. Please notify an Administrator of this error.")

            try:
                scheduler.remove_job('debt' + str(rid))
            except Exception as e:
                pass

            if debt is True:
                return jsonify("Check-in was successful, but the user has exceeded their rental period.")

        return jsonify("Check-in was successful.")


    def checkOutBicycle(self, form):
        try:
            rid = form['rid']
            rfid = form['rfid']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        wID = current_user.roleID
        if not rfid:
            return jsonify(Error="Bicycle was not scanned."), 400

        rDao = RentalDAO()
        bHand = BicycleHandler()
        bid = bHand.getBIDByRFID(rfid)
        if not bid:
            return jsonify(Error="A bicycle with the given arguments does not exist. "
                                 "Please verify the submitted arguments."), 400

        if rid is not None:
            rental = rDao.getRentalByID(rid)
            if rental is None:
                return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        else:
            try:
                email = form['email']
            except Exception as e:
                return jsonify(Error="No arguments given to identify the rental."), 400
            if email:
                uHand = UsersHandler()
                cHand = ClientHandler()
                uID = uHand.getUserIDByEmail(email)
                if uID is None:
                    return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
                cID = cHand.getCIDByUID(uID)
                if cID is None:
                    return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
                rid = rDao.getRentalByCIDCheckOut(cID)
            else:
                return jsonify(Error="No arguments given to identify the rental."), 400

        if not rid:
            return jsonify(Error="A rental with the given arguments does not exist. "
                                 "Please verify the submitted arguments."), 400
        bStatus = bHand.getStatusByID(bid)
        print(bStatus)
        if bStatus == 'AVAILABLE':
            try:
                bHand.updateStatusIsAvailable(bid, wID, rid)
            except Exception as e:
                return jsonify(Error="An error has occurred during bicycle reallocation."), 400
        elif bStatus == 'RESERVED':
            try:
                bHand.updateStatusIsReserved(bid, wID, rid)
            except Exception as e:
                return jsonify(Error="An error has occurred during bicycle reallocation."), 400
        else:
            return jsonify(Error="Bicycle is not in a condition to be rented."), 400

        try:
            scheduler.remove_job('rental' + str(rid))
            print("Rental" + str(rid) + " has been removed.")
        except Exception as e:
            pass
        token = rDao.getStripeToken(rid)

        # if token == "CASH":
        #     money2collect = rDao.getMoneyToCollect(rid)
        #     return jsonify("Check-out was successful. The client has chosen to pay in cash. Please collect $" + str(money2collect) +".")
        # else:
        return jsonify("Check-out was successful.")

    def getBIDByCIDAndPlate(self, cid, plate):
        rDao = RentalDAO()
        bid = rDao.getBIDByCIDAndPlate(cid, plate)
        return bid

    def getNewRentals(self, tid, payment):
        rDao = RentalDAO()
        rental_list = rDao.getNewRentals(tid, payment)
        return rental_list

    def swapBicycle(self, form):
        rDao = RentalDAO()
        try:
            rid = form["rID"]
            oldRFID = form["oldRFID"]
            newRFID = form["newRFID"]
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        if rid and oldRFID and newRFID:
            if oldRFID != newRFID:
                bHand = BicycleHandler()

                oldBID = rDao.get_rental_by_rid_and_rfid(rid, oldRFID)
                if oldBID is None:
                    return jsonify(Error="This bicycle is not linked to the provided information."), 400

                newBID = bHand.get_bicycle_for_swap(newRFID)
                if newBID is None:
                    return jsonify(Error="Bicycle is not in a condition to be rented."), 400

                try:
                    bHand.swapStatus(newBID, rid)
                    return jsonify("The bicycle swap was successful.")
                except Exception as e:
                    return jsonify(Error="An error has occurred.")
            else:
                return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
        else:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400


    def getPlan(self):
        rDao = RentalDAO()
        try:
            result = rDao.getPlan()
            return result
            pass
        except Exception as e:
           raise e

    def getOverduePlan(self):
        rDao = RentalDAO()
        try:
            result = rDao.getOverduePlan()
            return result
            pass
        except Exception as e:
            raise e

    def activeRental(self, form):
        rDao = RentalDAO()
        try:
            rfid = form['rfid']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
        bHand = BicycleHandler()
        cHand = ClientHandler()
        bid = bHand.getBIDByRFID(rfid)
        rid = rDao.getRIDByBID(bid)
        if rid:
            isLate = rDao.isLate(rid)
            cid = rDao.getClientByRID(rid)
            if isLate is None:
                pNumber = cHand.getPhoneNumber(cid)
                name = cHand.getName(cid)
                if pNumber is None:
                    return jsonify("The renter does not have a phone number. Please check in the bicycle.")
                else:
                    return jsonify("Please call this number (" + str(pNumber) + ") to contact the renter. Their name is " + name)
            else:
                cHand.setDebtorFlag(cid)
                return jsonify("This bicycle is currently rented, but has exceeded its rental period.")
        else:
            return jsonify("This bicycle is not linked to an active rental.")

    def didNotPay(self, form):
        try:
            rid = form['rid']
            rDao = RentalDAO()
            rDao.didNotPay(rid)
            return jsonify("The rentals have been canceled.")
        except Exception as e:
            return jsonify(Error="An error has occurred."), 400

    def getPaymentMethod(self, form):
        try:
            rid = form['rid']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
        rDao = RentalDAO()
        token = rDao.getTokenByRID(rid)
        if token is None:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
        else:
            if token == "CASH":
                money2collect = rDao.getMoneyToCollect(rid)
                return jsonify("The client has chosen to pay in cash. Please collect " + money2collect + ".")
            else:
                return jsonify("The client has already paid.")

    def webhook(self, data, headers):
        payload = data
        sig_header = headers.get('Stripe-Signature')
        rDao = RentalDAO()
        # print(request.headers)
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, hook_key
            )
            print(event)
            # print(event['type'] == 'invoice.payment_succeeded')
            # print(event['data']['object']['billing_reason'] != 'subscription_create')
            # print(event['data']['object']['amount_paid'])
            # print(event['data']['object']['charge'])
            # print(event['data']['object']['lines']['data']['subscription'])
            if event['type'] == 'invoice.payment_succeeded' and event['data']['object'][
                'billing_reason'] != 'subscription_create':
                cost = event['data']['object']['amount_paid']
                tokenID = event['data']['object']['charge']
                subscriptionID = event['data']['object']['lines']['data'][0]['subscription']
                tid = rDao.getTIDByToken(subscriptionID)
                if tid is None:
                    return jsonify(), 400
                rDao.insertCharge(tid, tokenID, cost)
            return jsonify(), 200
        except ValueError as e:
            # Invalid payload
            traceback.print_exc()
            return jsonify("Value ErrorError", 400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            traceback.print_exc()
            return jsonify("Error", 400)




