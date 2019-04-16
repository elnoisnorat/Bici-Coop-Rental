from flask import Flask, request, jsonify
#from handler.schedule import ScheduleHandler
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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
from config.validation import isWorker, isClient, hasRole, isAdmin, isWorkerOrAdmin, validPassword, validUpdatePassword
from config.encryption import SECRET_KEY
from model.user import User


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = SECRET_KEY

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

'''
    Route that returns the current user's name.
    Used for testing.
'''
@app.route('/currentUser')
@login_required
def hello_world():
    return 'Your name is ' + current_user.name

@app.route('/home')
def home():
    return 'Welcome Home'

#########################################################Worker#########################################################
'''
    Route used for the worker's login
'''
@app.route('/workerLogin', methods=["GET"])                                                     #1
@validPassword
def workerLogin():
    if current_user.is_authenticated:
        return jsonify(Error="Invalid/Missing username or password."), 401
    token = WorkerHandler().workerLogin(request.json)
    if token is -2:
        return jsonify(Error="Invalid/Missing username or password"), 401
    elif token is -1:
        return jsonify(Error="This account is currently locked."), 401
    elif token is -3:
        return jsonify(Error="This account is disabled."), 403
    elif token is -4:
        return jsonify(Error="Awaiting confirmation."), 403
    else:
        info = UsersHandler().getUserInfo(request.json['Email'], "W")
        user = User(info, "W")
        user.id = request.json["Email"] + "W"
        login_user(user)
        return token

'''
    Route used for the creation and modifications done to a bicycle.
'''
@app.route('/bicycle', methods=["POST", "PUT"])                                                 #2, 3
@login_required
@isWorkerOrAdmin
def bicycle():
    if request.method == "POST":
        return BicycleHandler().insert(request.json)
    elif request.method == "PUT":
        return BicycleHandler().update(request.json)

'''
    Route used for the check in process of a bicycle that is about to be returned.
'''
@app.route('/checkIn', methods=["PUT"])                                                         #4
@login_required
@isWorker
def checkIn():
    return RentalHandler().checkInBicycle(request.json)

'''
    Route used for the check out process of a bicycle that is about to be released to a client.
'''
@app.route('/checkOut', methods=["PUT"])                                                        #5
@login_required
@isWorker
def checkOut():
    return RentalHandler().checkOutBicycle(request.json)

'''
    Route used to receive the list of pending maintenance requests for the bicycles in the system.
'''
@app.route('/getMaintenance', methods=["GET"])                                                  #6
def bicycleDetails():
    return MaintenanceHandler().getMaintenance(request.json)

'''
    Route used to provide the maintenance that was requested for a bicycle .
'''
@app.route('/provideMaintenance', methods=["PUT"])                                              #7
def provideMaintenance():
    return MaintenanceHandler().provideMaintenance(request.json)

##########################################################Admin#########################################################
'''
    Route used for the login of an administrator.
'''
@app.route('/adminLogin', methods=["GET"])                                                      #8
@validPassword
def adminLogin():
    if current_user.is_authenticated:
        return jsonify(Error="Invalid/Missing username or password."), 401
    token = AdminHandler().adminLogin(request.json)
    if token is -2:
        return jsonify(Error="Invalid/Missing username or password"), 401
    elif token is -1:
        return jsonify(Error="This account is currently locked."), 403
    elif token is -4:
        return jsonify(Error="Awaiting confirmation."), 403
    else:
        info = UsersHandler().getUserInfo(request.json['Email'], "A")
        user = User(info, "A")
        user.id = request.json["Email"] + "A"
        login_user(user)
        return token

'''
    Route used for the creation of an administrator.
'''
@app.route('/createAdmin', methods=["POST"])                                                    #9
@login_required
@isAdmin
def createAdmin():
    return AdminHandler().insert(request.json)

'''
    Route used for the creation of a worker.
'''
@app.route('/createWorker', methods=["POST"])                                                   #10
@login_required
@isAdmin
def createWorker():
    return WorkerHandler().insert(request.json)

'''
    Route used to get an individual or list of workers.
'''
@app.route('/getWorker', methods=["GET"])                                                       #11
@login_required
@isAdmin
def getWorker():
    return WorkerHandler().getWorker(request.json)

'''
    Route used to update the status of a worker.
'''
@app.route('/updateWorkerStatus', methods=["PUT"])                                              #12
@login_required
@isAdmin
def updateWorkerStatus():
    return WorkerHandler().updateStatus(request.json)

'''
    Route used to edit the rental plans.
'''
@app.route('/editPlan', methods=["PUT"])                                                        #13
@login_required
@isAdmin
def editPlan():
    return RentalPlanHandler().editPlan(request.json)

@app.route('/getDecommissionRequest', methods=["GET"])                                          #14
def getDecommissionRequest():
    return

@app.route('/resolveDecommission', methods=["POST"])                                            #15
def resolveDecommission():
    return

#########################################################Client#########################################################
'''
    Route used for the creation of a user.
'''
@app.route('/client', methods=["POST"])                                                         #16
def createClient():
    return ClientHandler().insert(request.json)
'''
    Route used for the login process of a client.
'''
@app.route('/clientLogin', methods=["GET"])                                                     #17
@validPassword
def clientLogin():
    if current_user.is_authenticated:
        return jsonify(Error="Invalid/Missing username or password."), 401
    token = ClientHandler().clientLogin(request.json)
    if token is -2:
        return jsonify(Error="Invalid/Missing username or password"), 401
    elif token is -1:
        return jsonify(Error="This account is currently locked."), 403
    elif token is -4:
        return jsonify(Error="Awaiting confirmation."), 403
    else:
        info = UsersHandler().getUserInfo(request.json['Email'], "C")
        user = User(info, "C")
        user.id = request.json["Email"] + "C"
        login_user(user)
        return token

'''
    Route used for the creation of a bicycle rental.
'''
@app.route('/rentBicycle', methods=["POST"])                                                    #18
@login_required
@isClient
def rentBicycle():
    return TransactionHandler().newTransaction(request.json)


'''
    Route used to get the rental plans that have been established.
'''
@app.route('/getRentalPlan', methods=["GET"])                                                   #19
@login_required
@isClient
def getRentalPlan():
    return RentalPlanHandler().getRentalPlan()

'''
    Route used to view the current bicycle rentals that the client has.
'''
@app.route('/viewCurrentRental', methods = ["GET"])                                             #20
@login_required
@isClient
def viewCurrentRental():
    return RentalHandler().getRentalByCID(request.json)

'''
    Route used to request maintenance for a bicycle that is not in the system.
'''
@app.route('/requestPersonalMaintenance', methods=["POST"])                                     #21
@login_required
@isClient
def requestPersonalMaintenance():
    return ServiceMaintenanceHandler().requestServiceMaintenance(request.json)

#########################################################Everyone#########################################################
'''
    Route used to modify the name and last name of a user.
    Needs to receive both parameters
'''
@app.route('/updateName', methods=["PUT"])                                                      #22
@hasRole
@login_required
def updateName():   #Requires token (All)
    return UsersHandler().updateName(request.json)

'''
    Route used to view relevant information of the current user.
'''
@app.route('/profile', methods=["GET"])                                                         #23
@login_required
def profile():
    profile = {}
    profile["Name"] = current_user.name
    profile["Last Name"] = current_user.lName
    profile["Email"] = current_user.email
    profile["Phone Number"] = current_user.pNumber
    profile["Role"] = current_user.role
    profile["Role ID"] = current_user.roleID
    return jsonify(Profile=profile)

'''
    Route used to modify a user's password.
'''
@app.route('/updatePassword', methods=["PUT"])                                                  #24
@login_required
@hasRole
@validUpdatePassword
def updatePassword():
    return UsersHandler().updatePassword(request.json)

'''
    Route used to modify a user's phone number.
'''
@app.route('/updatePhoneNumber', methods=["PUT"])                                               #25
#@login_required
#@hasRole
def updatePhoneNumber():
    return UsersHandler().updatePNumber(request.json)

'''
    Route used to reset a user's password and send a new one via email.(The email part is not implemented)
'''
@app.route('/forgotPassword', methods=["PUT"])                                                  #26
def forgotPassword():
    if current_user.is_authenticated:
        return jsonify(), 404
    return UsersHandler().resetPassword(request.json)

'''
    Route used to confirm a new user account.
'''
@app.route('/confirm', methods=["PUT"])                                                         #27
def confirmAccount():
    return UsersHandler().confirmAccount(request.args)

#####################################################CLIENT&WORKER######################################################
'''
    Route used to request maintenace for a rented/stored bicycle.
'''
@app.route('/requestRentalMaintenance', methods=["POST"]) #Client and Worker                    #28
@login_required
def requestRentalMaintenance():
    return MaintenanceHandler().requestMaintenance(request.json)

#####################################################ADMIN&WORKER#######################################################
'''
    Route used to get a list of bicycles.
'''
@app.route('/bicycle', methods=["GET"])                                                         #29
@login_required
@isWorkerOrAdmin
def getbicycle():
    return BicycleHandler().getBicycle(request.json)

'''
    Route used to get a client list.
    (No actual use as of now)
'''
@app.route('/client', methods=['GET'])                                                          #30
#@login_required
def getClient():
    return ClientHandler().getClient(request.json)

'''
    Route used to make a decommission request
'''
@app.route('/requestDecommission', methods=["POST"])                                            #31
def requestDecommission():
    return

'''
    Route used for testing features.
'''
@app.route('/test')
def test():
    return ""

'''
    Route used to logout a user.
'''
@app.route('/logout', methods=["POST"])
@login_required
@hasRole
def logout():
    if current_user.role == "Worker":
        WorkerHandler().workerLogOut()
    logout_user()
    return jsonify('You are now logged out')

if __name__ == '__main__':
    app.run(debug=True)
