from flask import Flask, request, render_template
##from handler.worker import WorkerHandler
import stripe
from config.validation import isWorker
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
    data-description="Example charge"
    data-image="https://stripe.com/img/documentation/checkout/marketplace.png"
    data-locale="auto">
  </script>
</form>"""


@app.route('/pay', methods =['POST'])
def pay():
    customer  = stripe.Customer.create(email = request.form['stripeEmail'], source = request.form['stripeToken'])
    charge = stripe.Charge.create(customer=customer.id, amount = 9900, currency = 'usd', description='Bike' )
    return 'Thanks'



@app.route('/workerLogin')
def workerLogin():
    print(request.args)
    return WorkerHandler().workerLogin(request.json)




if __name__ == '__main__':
    app.run(debug=True)
