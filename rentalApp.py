import traceback

from app import app, login_manager, login_user, login_required, logout_user, current_user, request, jsonify, session, atexit, scheduler
from handler.client import ClientHandler
from handler.maintenance import MaintenanceHandler
from handler.rental import RentalHandler
from handler.rentalPlan import RentalPlanHandler
from handler.serviceMaintenance import ServiceMaintenanceHandler
from handler.transaction import TransactionHandler
from handler.worker import WorkerHandler
from handler.admin import AdminHandler
from handler.bicycle import BicycleHandler
from handler.user import UsersHandler
from handler.financial import FinancialHandler
from config.validation import isWorker, isClient, hasRole, isAdmin, isWorkerOrAdmin, validUpdatePassword, \
    validUpdatePhoneNumber, isWorkerOrClient, validUserCreation, validUpdateName, validUpdateLName, validUpdateNames
from config.encryption import SECRET_KEY, pKey
from model.user import User
from flask_cors import CORS
import re
import stripe
app.secret_key = SECRET_KEY
CORS(app, supports_credentials=True)

@login_manager.user_loader
def load_user(id):
    size = len(id)
    email = id[0:size-1]
    role = id[size-1]
    info = UsersHandler().getUserInfo(email, role)
    if not info:
        return
    user = User(info, role)
    return user

@app.route('/currentUser')
@login_required
def currentUser():
    """
    Route that returns the current user's name.
    Used for testing.
    :param:
    {}
    :return: A string with the name of the current user
    """
    return jsonify('Your name is ' + current_user.name)

@app.route('/home')
def home():
    """
    Route that returns a response object which contains a string
    :return: A dictionary that contains the string 'Welcome Home'
    """
    print('Welcome Home')
    return 'DONE'

#########################################################Worker#########################################################

@app.route('/workerLogin', methods=["GET"])                                                     #1
def workerLogin():
    """
    Route used for the worker's login
    :param:
    {
        "Email" = "",
        "password" = ""
    }
    :return: A response object which contains the users information
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400

    if current_user.is_authenticated:
        return jsonify(Error="Incorrect username or password."), 400

    token = WorkerHandler().workerLogin(request.json)
    if token is -1:
        return jsonify(Error="An error has occurred. Please contact an administrator."), 403

    elif token is -2:
        return jsonify(Error="Incorrect username or password"), 403

    elif token is -3:
        return jsonify(Error="An error has occurred. Please contact an administrator."), 403

    else:
        info = UsersHandler().getUserInfo(request.json['Email'], "W")
        user = User(info, "W")
        user.id = request.json["Email"] + "W"
        login_user(user)
        return token

"""
    Route used for the creation and modifications done to a bicycle.
"""
@app.route('/bicycle', methods=["POST"])                                                 #2
@login_required
@isWorkerOrAdmin
def bicycle():
    """
    Route used for the creation of a bicycle.
    :param:
    {
	    "lp" : "",
        "rfid" : "",
        "model" : "",
        "brand" : "",
        "snumber" : ""
    }
    :return: A message confirming the creation of the bicycle
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return BicycleHandler().insert(request.json)

@app.route('/bicycle', methods=["PUT"])                                                 #3
@login_required
@isWorkerOrAdmin
def bicycleUpdate():
    """
    Route used for the modifications of a bicycle.
    :param:
    {
	    "lp" : "",
	    "bikestatus" : "",
        "rfid" : "",
        "model" : "",
        "brand" : "",
    }
    :return: A message stating that the update was successful
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return BicycleHandler().update(request.json)

"""
    Route used for the creation and modifications done to a bicycle.
"""
@app.route('/bicyclesInInventory', methods=["GET"])                                                 #2, 3
@login_required
@isWorkerOrAdmin
def bicycleInInventory():
    """
    Route used to get the bicycles that are in the Inventory (ie bikestatus != rented, decommissioned)
    :param:
    {}
    :return: A response object that contains a list of all the bicycles that should be in the workspace
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return BicycleHandler().getAllBicyclesInPhysicalInventory()


"""
    Route used for the check in process of a bicycle that is about to be returned.
"""
@app.route('/checkIn', methods=["PUT"])                                                         #4
@login_required
@isWorker
def checkIn():
    """
    Route used for the check in process of a bicycle that is about to be returned.
    :param:
    {
        "rfid": "",
        "lp": "" (Optional: In case rfid malfunctions)
    }
    :return: Return confirmation that check-in was successful
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return RentalHandler().checkInBicycle(request.json)

"""
    Route used for the check out process of a bicycle that is about to be released to a client.
"""
@app.route('/checkOut', methods=["PUT"])                                                        #5
@login_required
@isWorker
def checkOut():
    """
    Route used for the check out process of a bicycle that is about to be released to a client.
    :param:
    {
        "rid": "",
        "rfid": "",
        "email": "", (Optional: For rental identification. Not in use.)
    }
    :return: Return confirmation that check-out was successful
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return RentalHandler().checkOutBicycle(request.json)

"""
    Route used to receive the list of pending maintenance requests for the bicycles in the system.
"""
@app.route('/getMaintenance', methods=["GET"])                                                  #6
@isWorker
def bicycleDetails():
    """
    Route used to receive the list of pending maintenance requests for the bicycles in the system.
    :param:
    {}
    :return: A response object with the maintenance requests  that have not been finished or a message stating that there are no current maintenance requests.
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return MaintenanceHandler().getMaintenance(request.json)

"""
    Route used to provide the maintenance that was requested for a bicycle .
"""
@app.route('/provideMaintenance', methods=["PUT"])                                              #7
@isWorker
def provideMaintenance():
    """
    Route used to provide the maintenance that was requested for a bicycle .
    :param:
    {
        "Notes": "",
        "Email": "",
        "mID": "",
        "lp": "",   (Optional: For the service New Plate)
        "rfid": ""  (Optional: For the service New RFID tag)
    }
    :return: A confirmation that the maintenance has been updated to show that it has been completed
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return MaintenanceHandler().provideMaintenance(request.json)

@app.route('/swapBicycle', methods=["PUT"])
@isWorker
def swapBicycle():
    """
    Route used for the exchange of bicycles in a rental request
    :param:
    {
        "rID": "",
        "oldRFID": "",
        "newRFID": ""
    }
    :return: A confirmation that the exchange was successful
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return RentalHandler().swapBicycle(request.json)

@app.route('/activeRental', methods=["PUT"])
@login_required
@isWorker
def activeRental():
    """
    Route used to check if a bicycle is currently linked to a rental
    :param:
    {
        "rfid": ""
    }
    :return: A message with the contact information of the renter if the bicycle is linked to an active rental,
             a message if the rental is past its due date.
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return RentalHandler().activeRental(request.json)

@app.route('/getPaymentMethod', methods=["GET"])
@login_required
@isWorker
def getPaymentMethod():
    """
    Route used to determine if a cash transaction is needed
    :param:
    {
        "rid": ""
    }
    :return: A message stating the type of transaction.
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return RentalHandler().getPaymentMethod(request.json)


@app.route('/didNotPay', methods=["PUT"])
@login_required
@isWorker
def didNotPay():
    """
    Route used to close a cash transaction that was not paid
    :param:
    {
        "rfid": ""
    }
    :return: A message confirming that the transaction was canceled.
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return RentalHandler().didNotPay(request.json)

##########################################################Admin#########################################################
"""
    Route used for the login of an administrator.
"""
@app.route('/adminLogin', methods=["GET"])                                                      #8
def adminLogin():
    """
    Route used for the login of an administrator.
    :param:
    {
        "Email": "",
        "password": ""
    }
    :return: A response object with the user's information
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400

    if current_user.is_authenticated:
        return jsonify(Error="Incorrect username or password."), 400
    token = AdminHandler().adminLogin(request.json)

    if token is -1:
        return jsonify(Error="An error has occurred. Please contact an administrator."), 403

    elif token is -2:
        return jsonify(Error="Incorrect username or password"), 403

    else:
        info = UsersHandler().getUserInfo(request.json['Email'], "A")
        user = User(info, "A")
        user.id = request.json["Email"] + "A"
        login_user(user)
        return token

"""
    Route used for the creation of an administrator.
"""
@app.route('/createAdmin', methods=["POST"])                                                    #9
@login_required
@isAdmin
@validUserCreation
def createAdmin():
    """
    Route used for the creation of an administrator.
    :param:
    {
        "FName" : "",
	    "LName" : "",
	    "Email": "",
	    "password" : "",
	    "PNumber" : ""
    }
    :return: A confirmation that the account was created.
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return AdminHandler().insert(request.json)

"""
    Route used for the creation of a worker.
"""
@app.route('/createWorker', methods=["POST"])                                                   #10
@login_required
@isAdmin
@validUserCreation
def createWorker():
    """
    Route used for the creation of a worker.
    :param:
    {
        "FName" : "",
	    "LName" : "",
	    "Email": "",
	    "password" : "",
	    "PNumber" : ""
    }
    :return: A confirmation that the account was created.
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return WorkerHandler().insert(request.json)

"""
    Route used to get an individual or list of workers.
"""
@app.route('/getWorker', methods=["GET"])                                                       #11
@login_required
@isAdmin
def getWorker():
    """
    Route used to get an individual or list of workers.
    :param:
    {
        (If empty gets all workers)
        "fName": "",    (Optional)
        "lName": "",    (Optional)
        "pNumber": "",  (Optional)
        "email": "",    (Optional)
        "wid": "",      (Optional)
        "uid": "",      (Optional)
        "status": "",   (Optional)
        "orderby": ""   (Optional)
    }
    :return: A list with the worker's information
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return WorkerHandler().getWorker(request.json)

@app.route('/getConfirmedWorker', methods=["GET"])                                                       #11
@login_required
@isAdmin
def getConfirmedWorker():
    """
    Route used to get a list of all workers that have been confirmed.
    :param:
    {}
    :return: A list with the worker's information
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return WorkerHandler().getConfirmedWorker()

"""
    Route used to update the status of a worker.
"""
@app.route('/updateWorkerStatus', methods=["PUT"])                                              #12
@login_required
@isAdmin
def updateWorkerStatus():
    """
    Route used to update the status of a worker.
    :param:
    {
        "wID": ""
    }
    :return: A confirmation that the update was successful
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return WorkerHandler().updateStatus(request.json)

@app.route('/getFinancialReport', methods=["GET"])
@login_required
@isAdmin
def getFinancialReport():
    """
    Route used to get the rentals and revenue earned in the past seven days
    :param:
    {}
    :return: The number of rentals in the past seven days and the amount of money earned
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return FinancialHandler().getFinancialReport(request.json)

@app.route('/getRentedBicycleList', methods=['GET'])
@login_required
@isAdmin
def getRentedBicycleList():
    return RentalHandler().getRentedBicycleList()


"""
    Route used to edit the rental plans.#############################################
"""
@app.route('/editPlan', methods=["PUT"])                                                        #13
@login_required
@isAdmin
def editPlan():
    """
    Route used to edit the rental plans.
    :param:
    {
        "name": "",
        "amount": ""
    }
    :return:
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return RentalPlanHandler().editPlan(request.json)

@app.route('/getDecommissionRequest', methods=["GET"])                                          #14
def getDecommissionRequest():
    return

@app.route('/resolveDecommission', methods=["POST"])                                            #15
def resolveDecommission():
    return

#########################################################Client#########################################################
"""
    Route used for the creation of a user.
"""
@app.route('/client', methods=["POST"])                                                         #16
@validUserCreation
def createClient():
    """
    Route used for the creation of a user.
    :param:
    {
        "FName" : "",
	    "LName" : "",
	    "Email": "",
	    "password" : "",
	    "PNumber" : ""
    }
    :return: A confirmation that the account was created.
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400
    return ClientHandler().insert(request.json)

"""
    Route used for the login process of a client.
"""
@app.route('/clientLogin', methods=["POST"])                                                     #17
def clientLogin():
    """
    Route used for the login of a client.
    :param:
    {
        "Email": "",
        "password": ""
    }
    :return: A response object with the user's information
    """
    if request.json is None:
        return jsonify(Error="An error has occurred."), 400

    if current_user.is_authenticated:
        return jsonify(Error="Incorrect username or password."), 400

    token = ClientHandler().clientLogin(request.json)

    if token is -1:
        return jsonify(Error="An error has occurred. Please contact an administrator."), 403

    elif token is -2:
        return jsonify(Error="Incorrect username or password"), 403

    else:
        info = UsersHandler().getUserInfo(request.json['Email'], "C")
        user = User(info, "C")
        user.id = request.json["Email"] + "C"
        login_user(user)
        return token

@app.route('/charge', methods=["POST", "GET"])
@login_required
@isClient
def charge():
    """
    Route used to determine the amount, payment and plan of the rental
    :param:
    {
        "amount": "",
        "payment": "",
        "plan": ""
    }
    :return: A redirect to the rentBicycle route
    """
    try:
        session['quantity'] = request.json['amount']
        session['payment'] = request.json['payment']
    except Exception as e:
        traceback.print_exc()
    return TransactionHandler().charge(request.json, request.args)

"""
    Route used for the creation of a bicycle rental.
"""
@app.route('/rentBicycle', methods=["POST"])                                                    #18
@login_required
@isClient
def rentBicycle():
    """
    Route used for the creation of a bicycle rental.
    :return: A messeage with the confirmation code of each bicycle rented
    """
    return TransactionHandler().newTransaction(request.json)


"""
    Route used to get the rental plans that have been established.
"""
@app.route('/getRentalPlan', methods=["POST"])                                                   #19
@login_required
@isClient
def getRentalPlan():
    return RentalPlanHandler().getRentalPlan()

"""
    Route used to view the current bicycle rentals that the client has.
"""
@app.route('/viewCurrentRental', methods = ["POST"])                                             #20
@login_required
@isClient
def viewCurrentRental():
    """
    Route used to view the current bicycle rentals that the client has.
    :param:
    {}
    :return: A response object which contains a list of the rentals.
    """
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return RentalHandler().getRentalByCID(request.json)

"""
    Route used to request maintenance for a bicycle that is not in the system.
"""
@app.route('/requestPersonalMaintenance', methods=["POST"])                                     #21
@login_required
@isClient
def requestPersonalMaintenance():
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return ServiceMaintenanceHandler().requestServiceMaintenance(request.json)

#########################################################Everyone#########################################################
@app.route('/updateNames', methods=["PUT"])                                                      #22
@hasRole
@login_required
@validUpdateNames
def updateNames():
    """
    Route used to modify the name and last name of a user.
    :param:
    {
        "FName": ""
    }
    :return: A response object with a message stating that the update was successful
    """
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return UsersHandler().updateNames(request.json)

"""
    Route used to modify the name of a user.
"""
@app.route('/updateName', methods=["PUT"])                                                      #22
@hasRole
@login_required
@validUpdateName
def updateName():
    """
    Route used to modify the name of a user.
    :param:
    {
        "FName": ""
    }
    :return: A response object with a message stating that the update was successful
    """
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return UsersHandler().updateName(request.json)

"""
    Route used to modify the last name of a user.
"""
@app.route('/updateLName', methods=["PUT"])                                                      #22
@hasRole
@login_required
@validUpdateLName
def updateLName():   #Requires token (All)
    """
    Route used to modify the name of a user.
    :param:
    {
        "LName": ""
    }
    :return: A response object with a message stating that the update was successful
    """
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return UsersHandler().updateLName(request.json)

"""
    Route used to view relevant information of the current user.
"""
@app.route('/profile', methods=["GET"])                                                         #23
@login_required
def profile():
    profile = {}
    profile["Name"] = current_user.name
    profile["Last Name"] = current_user.lName
    profile["Email"] = current_user.email
    profile["Phone Number"] = current_user.pNumber
    #profile["Role"] = current_user.role
    #profile["Role ID"] = current_user.roleID
    return jsonify(Profile=profile)

"""
    Route used to modify a user's password.
"""
@app.route('/updatePassword', methods=["PUT"])                                                  #24
@login_required
@hasRole
@validUpdatePassword
def updatePassword():
    """
    Route used to modify a user's password.
    :param:
    {
        "oldPassword": "",
        "newPassword": "",
        "confirmPassword": ""
    }
    :return:
    """
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return UsersHandler().updatePassword(request.json)

"""
    Route used to modify a user's phone number.
"""
@app.route('/updatePhoneNumber', methods=["PUT"])                                               #25
@login_required
@hasRole
@validUpdatePhoneNumber
def updatePhoneNumber():
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return UsersHandler().updatePNumber(request.json)

"""
    Route used to confirm a password reset request.
"""
@app.route('/confirmForgotPassword', methods=["POST"])
def confirmResetPassword():
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return UsersHandler().confirmForgotPassword(request.json)

"""
    Route used to reset a user's password and send a new one via email.(The email part is not implemented)
"""
@app.route('/forgotPassword')                                                                   #26
def forgotPassword():
    if request.args is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    if current_user.is_authenticated:
        return jsonify(Error="An error has occurred."), 400
    return UsersHandler().resetPassword(request.args)

"""
    Route used to confirm a new user account.
"""
@app.route('/confirm')                                                         #27
def confirmAccount():
    if request.args is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return UsersHandler().confirmAccount(request.args)

"""
    Route used to generate a new confirmation token.
"""
@app.route('/newConfirmation', methods=['POST'])
def newConfirmation():
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return UsersHandler().newConfirmation(request.json)

#####################################################CLIENT&WORKER######################################################
"""
    Route used to request maintenace for a rented/stored bicycle.
"""
@app.route('/requestRentalMaintenance', methods=["POST"]) #Client and Worker                    #28
@login_required
@isWorkerOrClient
def requestRentalMaintenance():
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

    return MaintenanceHandler().requestMaintenance(request.json)

#####################################################ADMIN&WORKER#######################################################
"""
    Route used to get a list of bicycles.
"""
@app.route('/bicycle', methods=["GET"])                                                         #29
@login_required
@isWorkerOrAdmin
def getbicycle():
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return BicycleHandler().getBicycle(request.json)

"""
    Route used to get a client list.
    (No actual use as of now)
"""
@app.route('/client', methods=['GET'])                                                          #30
@login_required
def getClient():
    if request.json is None:
        return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400
    return ClientHandler().getClient(request.json)

"""
    Route used to make a decommission request
"""
@app.route('/requestDecommission', methods=["POST"])                                            #31
def requestDecommission():
    return

@app.route('/webhook', methods=["POST"])
def webhook():
    return RentalHandler().webhook(request.data, request.headers)

@app.route('/dueNow',  methods =['GET'])
def dueNow():
    #Send Subscription ID of subscription to be sped up
    return jsonify(stripe.Subscription.modify(request.args.get('id'),
trial_end='now', prorate = False, quantity=2))
"""
    Route used for testing features.
"""
@app.route('/test')
def test():
    return "DONE"

@app.route('/sche')
def schedule():
    try:
        scheduler.get_jobs()
        scheduler.print_jobs()
    except:
        print("#F")
    return "DONE"


"""
    Route used to logout a user.
"""
@app.route('/logout', methods=["POST", "GET"])
@login_required
@hasRole
def logout():
    if current_user.role == "Worker":
        WorkerHandler().workerLogOut()
    logout_user()
    return jsonify('You are now logged out')

if __name__ == '__main__':
    app.run()
    #debug=True)#, ssl_context=('cert.pem', 'key.pem'))
