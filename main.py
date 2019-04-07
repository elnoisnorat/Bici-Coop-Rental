from flask import Flask, request, render_template, jsonify
from handler.worker import WorkerHandler
import stripe
import time
import datetime
from handler.client import ClientHandler
##from config.validation import isWorker
app = Flask(__name__)
sKey  = 'sk_test_qKdVTRj6NXM8EeLLUYnzXISS00K3MLJqu3'
pKey = 'pk_test_lYsQ0aji6IiOcMBI3qXU02Dd00XWDimuKZ'
stripe.api_key = sKey
@app.route('/')
def hello_world():
    return 'World!!!!!!'

@app.route('/home')

def home():
    return  """ <form action="http://127.0.0.1:5000/pay" method="POST">
  <script
    src="https://checkout.stripe.com/checkout.js" class="stripe-button"
    data-key="pk_test_lYsQ0aji6IiOcMBI3qXU02Dd00XWDimuKZ"
    data-amount="999"
    data-name="Demo Site"
    data-zip-code="true"
    data-description="Example charge"
    data-image="https://stripe.com/img/documentation/checkout/marketplace.png"
    data-locale="auto">
  </script>
</form>"""


@app.route('/pay', methods =['POST'])
def pay():
    #customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    #charge = stripe.Charge.create(customer=customer.id, amount=990, currency='usd', description='Bike')
    try:
        print("Getting Outcome...")
        customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
        #charge = stripe.Charge.create(customer=customer.id, amount=990, currency='usd', description='Bike')
        subscription = stripe.Subscription.create(
            customer=customer['id'],
            items=[{'plan': '2'}],
        )
        print("Getting Outcome...")
        #print("This is the charge: " + charge['outcome'])
        print(subscription)
        dt = datetime.datetime(2019, 4, 19)
        print(int(time.mktime(dt.timetuple())))
        stripe.Subscription.modify(
            subscription['id'],
            #quantity = 1,
            trial_end = int(time.mktime(dt.timetuple())),
            #prorate=False
            cancel_at_period_end=False,
            items=[{
                'id': subscription['items']['data'][0].id,
                'plan': '3',
            }]

        )
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
        #print(charge['outcome'])
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
        #print(charge['outcome'])
        pass
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        print('APIConnectionError')
        #print(charge['outcome'])
        pass
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        print('StripeError')
       #print(charge['outcome'])
        pass
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        print('Exception')
        #print(charge['outcome'])
        pass

    return "Done"


@app.route('/update', methods =['POST'])
def update():


    return "Done"


@app.route('/workerLogin')
def workerLogin():
    print(request.args)
    return WorkerHandler().workerLogin(request.json)


@app.route('/createUser', methods= ["POST"])
def createUser():

    print('Done')
    return ClientHandler().insert(request.json)

@app.route('/resetPassword', methods= ["POST"])
def resetPassword():

    print('Done')
    return ClientHandler().insert(request.json)





if __name__ == '__main__':
    app.run(debug=True)
