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
sKey  = 'sk_test_qKdVTRj6NXM8EeLLUYnzXISS00K3MLJqu3'
pKey = 'pk_test_lYsQ0aji6IiOcMBI3qXU02Dd00XWDimuKZ'
stripe.api_key = sKey
currentPlan = 2
@app.route('/home')
def hello_world():
    return 'World!!!!!!'

@app.route('/post', methods =['POST'] )
def post_test():
    return jsonify(request.json['hello'])


@app.route('/changeCard')

def ChangeCard():
    return  """ <form action='http://127.0.0.1:5000/update' method='POST'>
    <input type='hidden' name='cuid' value='cus_Er62nyLoykS7Co'/>
    <script
        src='https://checkout.stripe.com/checkout.js' class='stripe-button'
        data-key='pk_test_lYsQ0aji6IiOcMBI3qXU02Dd00XWDimuKZ'
        data-panel-label='Change Card'
        data-label='Change Card'
        data-name='Change Card'
        data-description='Change your card'
        data-billing-address='false'>
    </script>
</form>"""


@app.route('/charge')

def charge():
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


@app.route('/dueNow',  methods =['POST'])

def dueNow():
    #subcription =
    # stripe.Invoice.create(
    #     customer= subcription['customer'],
    # )

    #Send Subscription ID of subscription to be sped up
    return jsonify(stripe.Subscription.modify(str(request.json['id']),
                               billing_cycle_anchor='now', prorate = False

                               ))


@app.route('/pay', methods =['POST'])
def pay():
    #customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    #charge = stripe.Charge.create(customer=customer.id, amount=990, currency='usd', description='Bike')
    try:

        #print(request.json)
        print("Getting Outcome...")

        customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
        #charge = stripe.Charge.create(customer=customer.id, amount=990, currency='usd', description='Bike')
        subscription = stripe.Subscription.create(
            customer=customer['id'],
            items=[{'plan': str(RentalHandler().getPlan()[0])}],
        )
        print("Getting Outcome...")
        #print("This is the charge: " + charge['outcome'])
        print(subscription)
        #dt = datetime.datetime(2019, 4, 9,18, 50 )
        dt = datetime.datetime.today() + datetime.timedelta(weeks=1)
        print(int(time.mktime(dt.timetuple())))
        print("New Plan:\n")
        print(RentalHandler().getOverduePlan())
        stripe.Subscription.modify(
            subscription['id'],
            #quantity = 1,
            trial_end = int(time.mktime(dt.timetuple())),
            prorate = False,
            cancel_at_period_end=False,
            items=[{
                'id': subscription['items']['data'][0].id,
                'plan': str(RentalHandler().getOverduePlan()[0]) # Change to Overdue Plan
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
    except Exception :
        # Something else happened, completely unrelated to Stripe
        print('Exception')
        traceback.print_exc()
        #print(charge['outcome'])
        pass

    return "Done"


@app.route('/update', methods =['POST'])
def update():
    token = request.form['stripeToken']
    try:
        cuid = request.form['cuid'];

        # GET CUSTOMER ON FILE
        customer = stripe.Customer.retrieve(cuid)

        # CREATE NEW CARD THAT WAS JUST INPUTTED USING THE TOKEN
        card = customer.sources.create(source=token)

        # GET NEW CARD ID
        newcardID = card.id

        # SET CUSTOMER'S NEW CARD ID TO TO DEFAULT
        customer.default_source = newcardID

        # SAVE NEW CARD
        customer.save()
        return jsonify("Updated")
    except stripe.error.CardError as e:
        return jsonify("Updated")
    pass


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


@app.route('/webhooks', methods=['GET', 'POST'])
def webhook():

    # print("WebHookListener:\n" )
    # print(datetime.datetime.now())
    # print(request.json)
    try:
        print(request.json['data'])
        print(request.json['data']['object']['amount_remaining'])
        print
        if(request.json['type'] == "invoice.finalized" and int(request.json['data']['object']['amount_remaining']) > 0 ):

            return jsonify("Got It!")
        return jsonify("Nope...")
        pass
    except Exception :
        traceback.print_exc()
        return jsonify("Error")



    return jsonify(), 200





@app.route('/editOverduePlan', methods=['GET', 'POST'])

#Send JSON with Headers ['name'] and ['amount'],
def editOverduePlan():

    if request.method == 'GET':
        return jsonify(RentalHandler().getOverduePlan())
    if request.method == 'POST':
        #add  = request.json['Change']
        #plan = stripe.Plan.retrieve('3')
        #stripe.Plan.delete('3')

        #currentPlan = currentPlan +2
        ###
        #Method To Update Plan Reference Here
        ###


        return (RentalHandler().changeOverduePlan(request.json))
    return jsonify(), 200

@app.route('/editPlan', methods=['GET', 'POST'])
def editPlan():
    if request.method == 'GET':
        #try:
            result = RentalHandler().getPlan()
            return jsonify(result)
        #except Exception as e:
            #return jsonify(e)

    if request.method == 'POST':
        return (RentalHandler().changePlan(request.json))


@app.route('/addGrace', methods=['POST'])
def addGrace():
    dt = datetime.datetime(int(request.json['year']), int(request.json['month']), int(request.json['day']))
    return(jsonify(stripe.Subscription.modify(str(request.json['id']),
                               trial_end=int(time.mktime(dt.timetuple())),
                               #billing_cycle_anchor='now',
                               prorate = False

                               )))




if __name__ == '__main__':
    app.run(debug=True)
