from flask_login import current_user
from app import request, jsonify, session, scheduler
from dao.transaction import TransactionDAO
from handler.bicycle import BicycleHandler
from handler.rental import RentalHandler
from handler.client import ClientHandler
from handler.applicationScheduler import SchedulerHandler
from config.encryption import sKey, pKey
import stripe
import time
import datetime

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

    def charge(self, form):
        bHand = BicycleHandler()
        rHand = RentalHandler()
        try:
            cHand = ClientHandler()
            # amount = form['amount']
            # payment = form['payment']
            amount = form.get('amount')
            payment = form.get('payment')
            #plan = form['plan']
            session['quantity'] = amount
            session['payment'] = payment

            cid = current_user.roleID

            if cHand.getDebtorFlag(cid) is True:
                return jsonify(Error="An error has occurred."), 403

            available = bHand.getAvailableBicycleCount()
            if available < int(amount):
                session.pop('amount', None)
                session.pop('payment', None)
                return jsonify("We are sorry. At the moment there are not enough bicycles available for rent.")

            rentedAmount = rHand.getRentalAmountByCID(cid)
            if int(amount) + rentedAmount > 4:
                session.pop('amount', None)
                session.pop('payment', None)
                return jsonify("We are sorry, but you will exceed the maximum (4) rented bicycles allowed by our services.")

            return """ <form action="http://127.0.0.1:5000/rentBicycle" method="POST">
          <script
            src="https://checkout.stripe.com/checkout.js" class="stripe-button"
            data-key=""" + pKey + """
            data-amount="500"
            data-name="BiciCoop Rental"
            data-zip-code="true"
            data-description="Rental Transaction"
            data-image="https://stripe.com/img/documentation/checkout/marketplace.png"
            data-locale="auto">
          </script>
        </form>"""
        except Exception as e:
            session.pop('amount', None)
            session.pop('payment', None)
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

    def newTransaction(self):
        rHand = RentalHandler()
        amount = session['quantity']
        cid = current_user.roleID

        if amount is None or not amount.isnumeric():
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
        #Integration with the strip API static values for testing

        plan = RentalPlanHandler().getPlan()
        if plan is None:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        try:
            if session['payment'] == "CASH":
                cost = plan[1] * amount
                token = "CASH"

            elif session['payment'] == 'CARD':
                customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
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
                cost = subscription['items']['data'][0]['plan']['amount'] * amount
                token = subscription["id"]


            else:
                return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

            tDao = TransactionDAO()
            tid = tDao.newTransaction(token, cid, amount, cost, dt)
            rental_list = rHand.getNewRentals(tid, session['payment'])
            rentals = ""
            for rental in rental_list:
                rentals = rentals + str(rental[0]) + ", "
                if session['payment'] == "CASH":
                    # scheduler.add_job(func=SchedulerHandler().wasDispatched(), args=[rental[0]], trigger="date",
                    #                   run_date=rental[1], id='rental' + str(rental[0]))
                    #
                    # scheduler.add_job(func=SchedulerHandler().hasDebt(), args=[rental[0]], trigger="date",
                    #                   run_date=rental[2], id='debt' + str(rental[0]))

                    scheduler.add_job(func=SchedulerHandler().wasDispatched(), args=[rental[0]], trigger="date",
                                      run_date=datetime.datetime.today() + datetime.timedelta(minutes=2), id='rental' + str(rental[0]))

                    scheduler.add_job(func=SchedulerHandler().hasDebt(), args=[rental[0]], trigger="date",
                                      run_date=datetime.datetime.today() + datetime.timedelta(minutes=5), id='debt' + str(rental[0]))

                if session['payment'] == 'CARD':
                    # scheduler.add_job(func=SchedulerHandler().hasDebt(), args=[rental[0]], trigger="date",
                    #                   run_date=rental[1], id='rental' + str(rental[0]))
                    #
                    # scheduler.add_job(func=SchedulerHandler().hasDebt(), args=[rental[0]], trigger="date",
                    #                   run_date=rental[2], id='debt' + str(rental[0]))

                    scheduler.add_job(func=SchedulerHandler().hasDebt(), args=[rental[0]], trigger="date",
                                      run_date=datetime.datetime.today() + datetime.timedelta(minutes=2), id='rental' + str(rental[0]))

                    scheduler.add_job(func=SchedulerHandler().hasDebt(), args=[rental[0]], trigger="date",
                                      run_date=datetime.datetime.today() + datetime.timedelta(minutes=5), id='debt' + str(rental[0]))
            rentals[-2]
            session.pop('amount', None)
            session.pop('payment', None)
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
            pass
        session.pop('amount', None)
        session.pop('payment', None)
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

    def charge(self):
        pass


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