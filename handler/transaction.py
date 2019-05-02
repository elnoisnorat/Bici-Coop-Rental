import jwt
from flask import jsonify, abort, redirect, url_for
from flask_login import current_user

from dao.transaction import TransactionDAO
from config.encryption import SECRET_KEY
from handler.bicycle import BicycleHandler
from handler.rental import RentalHandler


class TransactionHandler:

    def build_transaction_dict(self, row):
        result = []
        result["tID"] = row[0]
        result["Stamp"] = row[1]
        result["Payment Method"] = row[2]['method']
        result["AmountPaid"] = row[2]['amount']
        result["ClientName"] = row[3]
        result["ClientLastName"] = row[4]
        result["Bike"] = row[5]
        #result["WorkerName"] = row[6]
        #result["WorkerLastName"] = row[7]

    def getAllTransactions(self):
        transDao = TransactionDAO()
        transactionList = transDao.getAllTransactions()
        resultList = []
        for row in transactionList:
            result = self.build_transaction_dict(row)
            resultList.append(result)
        return jsonify(Transactions=resultList)

    def getTransactionByClientId(self, cID):
        transDao = TransactionDAO()
        transactionList = transDao.getTransactionByClientId(cID)
        resultList = []
        for row in transactionList:
            result = self.build_transaction_dict(row)
            resultList.append(result)
        return jsonify(Transactions=resultList)

    def getTransactionByBicycleId(self, bID):
        transDao = TransactionDAO()
        transactionList = transDao.getTransactionsByBicycleId(bID)
        resultList = []
        for row in transactionList:
            result = self.build_transaction_dict(row)
            resultList.append(result)
        return jsonify(Transactions=resultList)

    def newTransaction(self, form):
        tDao = TransactionDAO()
        bHand = BicycleHandler()
        amount = form['amount']
        cid = current_user.roleID
        available = bHand.getAvailableBicycleCount()
        if available < int(amount):
            return jsonify("We are sorry. At the moment there are no bicycles available for rent.")

        #Integration with the strip API static values for testing
        stripeToken = redirect(url_for('pay'))
        cost = 9.99

        try:
            tid = tDao.newTransaction(stripeToken, cid, amount, cost)                    #Insert #1A
        except Exception as e:
            return jsonify(Error="An error has occurred."), 400

        rHand = RentalHandler()
        rental_list = rHand.getNewRentals(tid)
        rentals = ""
        for rental in rental_list:
            rentals = rentals + str(rental) + ", "
        rentals[-2]
        return jsonify("Rental(s) # " + rentals + " have been created successfully.")

'''
        def newTransactionWithCreditCard(self, form):
            tDao = TransactionDAO()
            bHand = BicycleHandler()
            pMethod = form['pMethod']
            if form['method'] == 'cash':
                token = \
                    {
                        "method": form['method'],
                        "amount": form['amount']
                    }
            elif form['method'] == 'creditCard':
                token = \
                    {
                        "method": form['method'],
                        "": form['charge']
                    }
            else:
                return jsonify(Error="Invalid payment method")

            form['Stripe']  # STRIPE CODE
            token = form['token']

            if bHand.getAvailableBicycleCount() <= 0:
                return jsonify("We are sorry. At the moment there are no bicycles available for rent.")

            
                #STRIPE CODE
            

            try:
                data = jwt.decode(token, SECRET_KEY)
                cid = data['cID']
            except:
                return jsonify(Error="Invalid token."), 401
            if not cid:
                return jsonify(Error="Client does not exist."), 401

            if pMethod == 'Cash':  # stripeToken not used
                tid = tDao.newTransactionWithCash(cid, pMethod)

            elif pMethod == 'CreditCard':
                tid = tDao.newTransactionWithCreditCard()
            else:
                return jsonify(Error="No payment method given."), 401

            rHandler = RentalHandler()

            rID = rHandler.rentBicycle(cid, tid)

            return jsonify(
                "Transaction # " + str(tid) + " and rental # " + str(rID) + " have been created successfully.")
'''