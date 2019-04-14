import base64
import jwt
import pickle
from flask import Flask, request, jsonify
#from handler.schedule import ScheduleHandler
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_rbac import RBAC, RoleMixin, UserMixin as userRBAC
from werkzeug.security import gen_salt

from handler.client import ClientHandler
from handler.maintenance import MaintenanceHandler
from handler.price import PriceHandler
from handler.rental import RentalHandler
from handler.rentalPlan import RentalPlanHandler
from handler.serviceMaintenance import ServiceMaintenanceHandler
from handler.transaction import TransactionHandler
from handler.worker import WorkerHandler
from handler.admin import AdminHandler
from handler.bicycle import BicycleHandler
from handler.user import UsersHandler
from config.validation import isWorker, isClient, hasRole, isAdmin
from config.encryption import SECRET_KEY
from config.dbconfig import db_string
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

@app.route('/currentUser')
@login_required
def hello_world():
    return 'The current user role is ' + current_user.name

@app.route('/home')
#@rbac.allow(roles=['client'], methods=['GET'])
#@isWorker
def home():
    return 'Welcome Home'

#########################################################Worker#########################################################
@app.route('/workerLogin')
def workerLogin():
    if current_user.is_authenticated:
        return jsonify("User already logged in.")
    token = WorkerHandler().workerLogin(request.json)
    if token is -2:
        return jsonify(Error="Invalid/Missing username or password")
    elif token is -1:
        return jsonify(Error="This account is currently locked.")
    else:
        info = UsersHandler().getUserInfo(request.json['Email'], "W")
        user = User(info, "W")
        user.id = request.json["Email"] + "W"
        login_user(user)
        return token

@app.route('/bicycle', methods=["POST", "PUT"])
#@isWorkerOrAdmin
#@login_required
def bicycle():
    if request.method == "POST":
        return BicycleHandler().insert(request.json)
    elif request.method == "PUT":
        return BicycleHandler().update(request.json)

@app.route('/checkIn', methods=["PUT"])
#@isWorker
#@login_required
def checkIn():
    return RentalHandler().checkInBicycle(request.json)

@app.route('/checkOut', methods=["PUT"])
#@isWorker
#@login_required
def checkOut():
    return RentalHandler().checkOutBicycle(request.json)

@app.route('/bicycleDetails')
def bicycleDetails():
    return MaintenanceHandler().getMaintenance(request.json)

@app.route('/provideMaintenance')
def provideMaintenance():
    return MaintenanceHandler().provideMaintenance(request.json)

@app.route('/requestDecommission')





##########################################################Admin#########################################################
@app.route('/adminLogin')
def adminLogin():
    if current_user.is_authenticated:
        return jsonify("User already logged in.")
    token = AdminHandler().adminLogin(request.json)
    if token is -2:
        return jsonify(Error="Invalid/Missing username or password")
    elif token is -1:
        return jsonify(Error="This account is currently locked.")
    else:
        info = UsersHandler().getUserInfo(request.json['Email'], "A")
        user = User(info, "A")
        user.id = request.json["Email"] + "A"
        login_user(user)
        return token

@app.route('/createAdmin')
#@isAdmin
#@login_required
def createAdmin():
    return AdminHandler().insert(request.json)

@app.route('/createWorker', methods=["POST"])
#@isAdmin
#@login_required
def createWorker():
    return WorkerHandler().insert(request.json)

@app.route('/getWorker', methods=["GET"])
#@isAdmin
def getWorker():
    return WorkerHandler().getWorker(request.json)

@app.route('/updateWorkerStatus')
#@isAdmin
#@login_required
def updateWorkerStatus():
    return WorkerHandler().updateStatus(request.json)



@app.route('/editPlan')
#@isAdmin
#@login_required
def editPlan():
    return RentalPlanHandler().editPlan(request.json)

#########################################################Client#########################################################
@app.route('/client', methods=["POST"])  #Verify if it needs to be split up
def createClient():
    if request.method == "POST":
        return ClientHandler().insert(request.json)
    else:
        return jsonify(Error="Invalid method")

@app.route('/clientLogin', methods=["GET"])
def clientLogin():
    #if current_user.is_authenticated:
    #    return jsonify("User already logged in.")
    token = ClientHandler().clientLogin(request.json)
    if token is -2:
        return jsonify(Error="Invalid/Missing username or password")
    elif token is -1:
        return jsonify(Error="This account is currently locked.")
    else:
        info = UsersHandler().getUserInfo(request.json['Email'], "C")
        user = User(info, "C")
        user.id = request.json["Email"] + "C"
        login_user(user)
        return token

@app.route('/rentBicycle', methods=["POST"])
#@isClient
#@login_required
def rentBicycle():
    if request.method == "POST":
        return TransactionHandler().newTransaction(request.json)
    else:
        return jsonify(Error="Invalid method."), 401


@app.route('/getPrice')	#View price of Bicycles
#@isClient
#@login_required
def viewPrice():
    return PriceHandler().getPrice()

@app.route('/getRentalPlan')
#@isClient
#@login_required
def getRentalPlan():
    return RentalPlanHandler().getRentalPlan()

@app.route('/viewCurrentRental', methods = ["GET"])
#@isClient
#@login_required
def viewCurrentRental():
    return RentalHandler().getRentalByCID(request.json)


@app.route('/requestPersonalMaintenance')
#@isClient
#@login_required
def requestPersonalMaintenance():
    return ServiceMaintenanceHandler().requestServiceMaintenance(request.json)

#########################################################Everyone#########################################################
@app.route('/updateName')
#@hasRole
#@login_required
def updateName():   #Requires token (All)
    return UsersHandler().updateName(request.json)

@app.route('/profile')
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

@app.route('/updatePassword')
#@login_required
#@hasRole
def updatePassword():
    return UsersHandler().updatePassword(request.json)

@app.route('/updatePhoneNumber')
#@login_required
#@hasRole
def updatePhoneNumber():
    return UsersHandler().updatePNumber(request.json)

@app.route('/forgotPassword', methods=["GET"])
def forgotPassword():
    if current_user.is_authenticated:
        return jsonify("User logged in. Please use update password.")
    return UsersHandler().resetPassword(request.json)

@app.route('/confirm', methods=["GET"])
def confirmAccount():
    return UsersHandler().confirmAccount(request.args)

#####################################################CLIENT&WORKER######################################################
@app.route('/requestRentalMaintenance', methods=["POST"]) #Client and Worker
#@login_required
def requestRentalMaintenance():
    return MaintenanceHandler().requestMaintenance(request.json)

#####################################################ADMIN&WORKER#######################################################
@app.route('/bicycle', methods=["GET"])
#@isWorkerOrAdmin
#@login_required
def getbicycle():
    return BicycleHandler().getBicycle(request.json)

@app.route('/client', methods=['GET'])  #Admin probably
#@login_required
def getClient():
    if request.method == "GET":
        return ClientHandler().getClient(request.json)
    else:
        return jsonify(Error="Invalid method")

@app.route('/test')
def test():
    email = "bbob21308@gmail.com"
    code_64 = base64.b64encode(email.encode())
    token = {"data": code_64}
    link = "localhost:5000/confirm?value="
    #code_64 = pickle.dumps(code)
    print(link)
    print(base64.b64decode(code_64))
    #test = ScheduleHandler().testSchedule()
    #return test

    return "Done"



@app.route('/logout')       #Make seperate log out  for worker
#@hasRole
@login_required
def logout():
    if current_user.role == "Worker":
        WorkerHandler().workerLogOut(current_user.email)
    logout_user()
    return jsonify('You are now logged out')

'''
@app.route('/workerLogOut')
@login_required
def workerLogOut():
    email = current_user.id
    WorkerHandler().workerLogOut(email)
    return jsonify("Worker has logged out.")
'''
if __name__ == '__main__':
    app.run(debug=True)
