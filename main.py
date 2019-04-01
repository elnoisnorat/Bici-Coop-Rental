from flask import Flask, request, jsonify

from handler.client import ClientHandler
from handler.maintenance import MaintenanceHandler
from handler.price import PriceHandler
from handler.rental import RentalHandler
from handler.serviceMaintenance import ServiceMaintenanceHandler
from handler.transaction import TransactionHandler
from handler.worker import WorkerHandler
from handler.admin import AdminHandler
from handler.bicycle import BicycleHandler
from handler.user import UsersHandler
from config.validation import isWorker, isAdmin, isClient
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Za World!!!!!!'

@app.route('/home')
@isWorker
def home():
    return 'Welcome Home'

#########################################################Worker#########################################################
@app.route('/workerLogin')
def workerLogin():
    return WorkerHandler().workerLogin(request.json)

@app.route('/bicycle', methods=["GET", "POST", "PUT"])
def bicycle():
    if request.method == "GET":
        return BicycleHandler().getBicycle(request.json)
    elif request.method == "POST":
        return BicycleHandler().insert(request.json)
    elif request.method == "PUT":
        return BicycleHandler().update(request.json)

@app.route('/checkIn', methods=["PUT"])
def checkIn():
    return RentalHandler().checkInBicycle(request.json)

@app.route('/chckOut', methods=["PUT"])
def checkOut():
    return RentalHandler().checkOutBicycle(request.json)



##########################################################Admin#########################################################
@app.route('/adminLogin')
def adminLogin():
    return AdminHandler().adminLogin(request.json)

@app.route('/createWorker', methods=["POST"])
def createWorker():
    return WorkerHandler().insert(request.json)

@app.route('/getWorker', methods=["GET"])
def getWorker():
    return WorkerHandler().getWorker(request.args)

#########################################################Client#########################################################
@app.route('/client', methods=["POST"])  #Verify if it needs to be split up
def createClient():
    if request.method == "POST":
        return ClientHandler().insert(request.json)
    else:
        return jsonify(Error="Invalid method")

@app.route('/clientLogin', methods=["GET"])
def clientLogin():
    return ClientHandler().clientLogin(request.json)


@app.route('/rentBicycle', methods=["POST"])
@isClient
def rentBicycle():
    if request.method == "POST":
        return TransactionHandler().newTransaction(request.json)
    else:
        return jsonify(Error="Invalid method."), 401


@app.route('/viewPrice')	#View price of Bicycles
@isClient
def viewPrice():
    return PriceHandler().getPrice()

@app.route('/viewCurrentRental', methods = ["GET"])
@isClient
def viewCurrentRental():
    return RentalHandler().getRentalByCID(request.json)


@app.route('/requestPersonalMaintenance')
@isClient
def requestPersonalMaintenance():
    return ServiceMaintenanceHandler().requestServiceMaintenance(request.json)

#########################################################Everyone#########################################################
@app.route('/updateName')
def updateName():   #Requires token (All)
    return UsersHandler().updateName(request.json)

@app.route('/updatePassword')   #If token... Else Email
def updatePassword():
    return

#####################################################CLIENT&WORKER######################################################
@app.route('/requestRentalMaintenance', methods=["POST"]) #Client and Worker
def requestRentalMaintenance():
    return MaintenanceHandler().requestMaintenance(request.json)

@app.route('/client', methods=['GET'])  #Admin probably
def getClient():
    if request.method == "GET":
        return ClientHandler().getClient(request.args)
    else:
        return jsonify(Error="Invalid method")

@app.route('/test')
def test():

    dict = {
        "user" : "BOB"
    }

    test = []
    test.append(dict['user'])
    print(dict['user'] + "-----" + test[0])

    return jsonify("DONE")

if __name__ == '__main__':
    app.run(debug=True)
