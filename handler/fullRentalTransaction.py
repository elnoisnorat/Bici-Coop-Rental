import jwt
from flask import jsonify, abort, redirect, url_for
from flask_login import current_user

from dao.transaction import TransactionDAO
from config.encryption import SECRET_KEY
from handler.bicycle import BicycleHandler
from handler.rental import RentalHandler
import datetime

from flask import Flask, request, render_template, jsonify
from handler.worker import WorkerHandler
import stripe
import time
import traceback
import datetime
from handler.client import ClientHandler
from handler.rental import RentalHandler

##from config.validation import isWorker
app = Flask(__name__)
sKey = 'sk_test_qKdVTRj6NXM8EeLLUYnzXISS00K3MLJqu3'
pKey = 'pk_test_lYsQ0aji6IiOcMBI3qXU02Dd00XWDimuKZ'
stripe.api_key = sKey
currentPlan = 2

from config.dbconfig import pg_config
import psycopg2

class FullTransactionHandler:
    def __init__(self):
         connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
         self.conn = psycopg2._connect(connection_url)

    def newTransaction(self):
        bHand = BicycleHandler()
        amount = 1#form['amount']
        cid = 1 #current_user.roleID
        available = bHand.getAvailableBicycleCount()
        if available < int(amount):
            return jsonify("We are sorry. At the moment there are no bicycles available for rent.")

        #Integration with the strip API static values for testing
        try:

            # print(request.json)
            print("Getting Outcome...")

            customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
            # charge = stripe.Charge.create(customer=customer.id, amount=990, currency='usd', description='Bike')
            subscription = stripe.Subscription.create(
                customer=customer['id'],
                items=[{'plan': str(RentalHandler().getPlan()[0])}],
            )
            print("Getting Outcome...")
            # print("This is the charge: " + charge['outcome'])
            print(subscription)
            # dt = datetime.datetime(2019, 4, 9,18, 50 )
            dt = datetime.datetime.today() + datetime.timedelta(weeks=1)
            print(int(time.mktime(dt.timetuple())))
            print("New Plan:\n")
            print(RentalHandler().getOverduePlan())
            stripe.Subscription.modify(
                subscription['id'],
                # quantity = 1,
                trial_end=int(time.mktime(dt.timetuple())),
                prorate=False,
                cancel_at_period_end=False,
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'plan': str(RentalHandler().getOverduePlan()[0])  # Change to Overdue Plan
                }]

            )
            cost = subscription['items']['data'][0]['plan']['amount']
            tDao = TransactionDAO()
            tid = tDao.newTransaction(subscription, cid, amount, cost)
            rHand = RentalHandler()
            rental_list = rHand.getNewRentals(tid)
            rentals = ""
            for rental in rental_list:
                rentals = rentals + str(rental) + ", "
            rentals[-2]
            return jsonify("Rental(s) # " + rentals + " have been created successfully.")
            pass
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})

            print("Status is: %s" % e.http_status)
            print("Type is: %s" % err.get('type'))
            print("Code is: %s" % err.get('code'))
            # param is '' in this case
            print("Param is: %s" % err.get('param'))
            print("Message is: %s" % err.get('message'))
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            print('RateLimitError')
            # print(charge['outcome'])
            pass
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print('InvalidRequestError')
            print(e)
            pass
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            print('AuthenticationError')
            # print(charge['outcome'])
            pass
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            print('APIConnectionError')
            # print(charge['outcome'])
            pass
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            print('StripeError')
            # print(charge['outcome'])
            pass
        except Exception:
            # Something else happened, completely unrelated to Stripe
            print('Exception')
            traceback.print_exc()
            # print(charge['outcome'])
            pass
        return jsonify("Done")