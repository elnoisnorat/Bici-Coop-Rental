from flask_login import current_user

from dao.transaction import TransactionDAO
from handler.bicycle import BicycleHandler

from flask import Flask, request, jsonify, session
import stripe
import time
import datetime
from handler.client import ClientHandler
from handler.rental import RentalHandler

app = Flask(__name__)
sKey = 'sk_test_qKdVTRj6NXM8EeLLUYnzXISS00K3MLJqu3'
pKey = 'pk_test_lYsQ0aji6IiOcMBI3qXU02Dd00XWDimuKZ'
stripe.api_key = sKey
currentPlan = 2

class FullTransactionHandler:
    def newTransaction(self):
        bHand = BicycleHandler()
        rHand = RentalHandler()
        amount = session['quantity']
        print(amount)
        cid = current_user.roleID
        cHand = ClientHandler()
        if cHand.getDebtorFlag(cid) is True:
            return jsonify(Error="An error has occurred."), 403
        if amount is None or not amount.isnumeric():
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
        #Integration with the strip API static values for testing
        try:

            print("Getting Outcome...")

            customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
            subscription = stripe.Subscription.create(
                customer=customer['id'],
                items=[{'plan': str(RentalHandler().getPlan()[0]),
                        'quantity': amount,
                        }],
            )
            print("Getting Outcome...")
            print(subscription)
            dt = datetime.datetime.today() + datetime.timedelta(weeks=1)
            print(int(time.mktime(dt.timetuple())))
            print("New Plan:\n")
            print(RentalHandler().getOverduePlan())
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
            rentedAmount = rHand.getRentalAmountByCID(cid)
            if int(amount) + rentedAmount > 4:
                return jsonify("We are sorry, but you will exceed the maximum(4) rented bicycles allowed by our services.")

            available = bHand.getAvailableBicycleCount()
            if available < int(amount):
                return jsonify("We are sorry. At the moment there are no bicycles available for rent.")

            tDao = TransactionDAO()
            tid = tDao.newTransaction(subscription["id"], cid, amount, cost)
            rental_list = rHand.getNewRentals(tid)
            rentals = ""
            for rental in rental_list:
                rentals = rentals + str(rental) + ", "
            rentals[-2]
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
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400