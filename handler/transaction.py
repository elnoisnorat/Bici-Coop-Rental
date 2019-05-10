import traceback

from flask_login import current_user
from app import request, jsonify, session, scheduler, redirect, url_for
from dao.transaction import TransactionDAO
from handler.bicycle import BicycleHandler
from handler.rental import RentalHandler
from handler.client import ClientHandler
from handler.applicationScheduler import SchedulerHandler
from config.encryption import sKey, pKey
from config.account import AWS_LINK
import stripe
import time
import datetime
import requests

from handler.rentalPlan import RentalPlanHandler

stripe.api_key = sKey
currentPlan =  2

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

    # def getAllTransactions(self):
    #     transDao = TransactionDAO()
    #     transactionList = transDao.getAllTransactions()
    #     resultList = []
    #     for row in transactionList:
    #         result = self.build_transaction_dict(row)
    #         resultList.append(result)
    #     return jsonify(Transactions=resultList)

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

    # def charge(self, form, args):
    #     bHand = BicycleHandler()
    #     rHand = RentalHandler()
    #
    #     try:
    #         amount = form['amount']
    #         payment = form['payment']
    #         # plan = form['plan']
    #     except Exception as e:
    #         pass
    #         # amount = args.get('amount')
    #         # payment = args.get('payment')
    #
    #
    #     try:
    #         cHand = ClientHandler()
    #
    #         # session['quantity'] = amount
    #         # session['payment'] = payment
    #
    #         cid = current_user.roleID
    #
    #         if cHand.getDebtorFlag(cid) is True:
    #             return jsonify(Error="An error has occurred."), 403
    #
    #         available = bHand.getAvailableBicycleCount()
    #         if available < int(amount):
    #             session.pop('amount', None)
    #             session.pop('payment', None)
    #             return jsonify("We are sorry. At the moment there are not enough bicycles available for rent.")
    #
    #         rentedAmount = rHand.getRentalAmountByCID(cid)
    #         if int(amount) + rentedAmount > 4:
    #             session.pop('amount', None)
    #             session.pop('payment', None)
    #             return jsonify("We are sorry, but you will exceed the maximum (4) rented bicycles allowed by our services.")
    #         if payment == 'CARD':
    #             return redirect(url_for('rentBicycle'), code=307)
    #
    #         else:
    #             return redirect(url_for('rentBicycle'), code=307)
    #     except Exception as e:
    #         traceback.print_exc()
    #         session.pop('amount', None)
    #         session.pop('payment', None)
    #         return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

    def newTransaction(self, form):
        bHand = BicycleHandler()
        rHand = RentalHandler()

        try:
            amount = form['amount']
            payment = form['payment']
            reqPlan = form['plan']
            if payment == 'CARD':
                stripeID = form['id']['id']
        except Exception as e:
            traceback.print_exc()
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        cHand = ClientHandler()

        cid = current_user.roleID
        email = current_user.email
        if cHand.getDebtorFlag(cid) is True:
            return jsonify(Error="An error has occurred. Please contact an administrator."), 403

        available = bHand.getAvailableBicycleCount()
        if available < int(amount):
            return jsonify("We are sorry. At the moment there are not enough bicycles available for rent.")

        rentedAmount = rHand.getRentalAmountByCID(cid)
        if int(amount) + rentedAmount > 4:
            return jsonify("We are sorry, but you will exceed the maximum of 4 rented bicycles allowed by our services.")

        rHand = RentalHandler()
        cid = current_user.roleID

        #Integration with the strip API static values for testing

        plan = RentalPlanHandler().getPlan(reqPlan)
        if plan is None:
            return jsonify(Error="No valid plan was selected."), 400

        try:
            if payment == "CASH":
                total = int(plan[1]) * int(amount)
                token = "CASH"
                dt = datetime.datetime.today() + datetime.timedelta(weeks=1)

            elif payment == 'CARD':
                customer = stripe.Customer.create(email= email, source= stripeID)
                subscription = stripe.Subscription.create(
                    customer=customer['id'],
                    items=[{'plan': str(plan[0]),
                            'quantity': amount,
                            }],
                )
                dt = datetime.datetime.today() + datetime.timedelta(weeks=1)
                stripe.Subscription.modify(
                    subscription['id'],
                    trial_end=int(time.mktime(dt.timetuple())),
                    prorate=False,
                    cancel_at_period_end=False,
                    items=[{
                        'id': subscription['items']['data'][0].id,
                        'plan': str(RentalHandler().getOverduePlan()[0]),  # Change to Overdue Plan
                        'quantity': amount,
                    }]

                )
                cost = subscription['items']['data'][0]['plan']['amount']
                token = subscription["id"]
                total = int(cost) * int(amount)

            else:
                return jsonify(Error="A valid payment method was not selected."), 400

            tDao = TransactionDAO()
            tid = tDao.newTransaction(token, cid, amount, total, dt)
            # rental_list = rHand.getNewRentals(tid, session['payment'])
            rental_list = rHand.getNewRentals(tid, payment)
            rentals = ""
            for rental in rental_list:
                rentals = rentals + str(rental[0]) + ", "
                # if session['payment'] == "CASH":
                if payment == "CASH":
                    scheduler.add_job(func=SchedulerHandler().wasDispatched, args=[rental[0]], trigger="date",
                                      run_date=rental[1], id='rental' + str(rental[0]))

                    scheduler.add_job(func=SchedulerHandler().hasDebt, args=[rental[0]], trigger="date",
                                      run_date=rental[2], id='debt' + str(rental[0]))

                    # scheduler.add_job(SchedulerHandler().wasDispatched, rental[0], trigger="date",
                    #                   run_date=datetime.datetime.today() + datetime.timedelta(seconds=10), id='rental' + str(rental[0]))

                    # scheduler.add_job(SchedulerHandler().hasDebt, rental[0], trigger="date",
                    #                   run_date=datetime.datetime.today() + datetime.timedelta(minutes=5), id='debt' + str(rental[0]))

                # if session['payment'] == 'CARD':
                if payment == 'CARD':
                    scheduler.add_job(func=SchedulerHandler().wasDispatched, args=[rental[0]], trigger="date",
                                      run_date=rental[1], id='rental' + str(rental[0]))

                    scheduler.add_job(func=SchedulerHandler().hasDebt, args=[rental[0]], trigger="date",
                                      run_date=rental[2], id='debt' + str(rental[0]))

                    # scheduler.add_job(SchedulerHandler().wasDispatched, args=[rental[0]], trigger="date",
                    #                   run_date=(datetime.datetime.today() + datetime.timedelta(seconds=30)), id='rental' + str(rental[0]))

                    # scheduler.add_job(func=SchedulerHandler().hasDebt, args=[rental[0]], trigger="date",
                    #                   run_date=(datetime.datetime.today() + datetime.timedelta(seconds=45)), id='debt' + str(rental[0]))

            rentals = rentals[:-2]
            # session.pop('amount', None)
            # session.pop('payment', None)
            return jsonify("Rental(s) # " + rentals + " have been created successfully.")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            pass
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            print('RateLimitError')
            pass
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print('InvalidRequestError')
            pass
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            print('AuthenticationError')
            pass
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            print('APIConnectionError')
            pass
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            print('StripeError')
            pass
        except Exception:
            # Something else happened, completely unrelated to Stripe
            print('Exception')
            traceback.print_exc()
            pass
        # session.pop('amount', None)
        # session.pop('payment', None)
        return jsonify(Error="An error has occurred."), 400
