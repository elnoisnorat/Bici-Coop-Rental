import jwt
from flask import Flask, request, jsonify
#from handler.schedule import ScheduleHandler
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_rbac import RBAC, RoleMixin, UserMixin as userRBAC
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
from flask_sqlalchemy import SQLALCHEMY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']
login_manager = LoginManager()
login_manager.init_app(app)
rbac = RBAC()

app.secret_key = SECRET_KEY
db = SQLALCHEMY(app)

class User(UserMixin, userRBAC, db.model):
    id = db.Column


class Role(RoleMixin):
    pass

client = Role('client')
worker = Role('worker')

@app.route('/currentUser')
@login_required
def hello_world():
    return 'The current user is ' + current_user.id

@app.route('/home')
@rbac.allow(roles=['worker'], methods=['GET'])
#@isWorker
def home():
    return 'Welcome Home'

#########################################################Worker#########################################################
@app.route('/workerLogin')
def workerLogin():
    token = WorkerHandler().workerLogin(request.json)
    if token is None:
        return jsonify(Error="Invalid/Missing username or password")
    else:
        user = User()
        user.id = request.json['Email']
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



##########################################################Admin#########################################################
@app.route('/adminLogin')
def adminLogin():
    token = AdminHandler().adminLogin(request.json)
    if token is None:
        return jsonify(Error="Invalid/Missing username or password")
    else:
        user = User()
        user.id = request.json['Email']
        login_user(user)
        return token

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
    return updateWorkerStatus(request.json)

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
    token = ClientHandler().clientLogin(request.json)
    if token is None:
        return jsonify(Error="Invalid/Missing username or password")
    else:

        user = User()
        user.id = request.json['Email']
        #user.add_role(client)
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
def profile():
    return current_user

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

@app.route('/forgotPassword')
def forgotPassword():
    return UsersHandler.resetPassword(request.json)

@app.route('/confirm/<string:confirmation>')
def confirmAccount(confirmation):
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
        return ClientHandler().getClient(request.args)
    else:
        return jsonify(Error="Invalid method")

@app.route('/test')
def test():
    #test = ScheduleHandler().testSchedule()
    #return test
    user = UsersHandler().getUserByEmail(request.json['email'])
    return jsonify(user)

@login_manager.user_loader
def load_user(email):
    if not UsersHandler().getUserByEmail(email):
        return

    user = User()
    user.id = email
    return user

@app.route('/logout')
#@hasRole
@login_required
def logout():
    logout_user()
    try:
        data = jwt.decode(request.json['token'], SECRET_KEY)
        if (data['Role'] == 'Worker'):
            WorkerHandler().workerLogOut(data['wID'])
    except:
        jsonify(Error="Invalid token")


    return jsonify('You are now logged out')


if __name__ == '__main__':
    app.run(debug=True)
