from dao.bicycle import BicycleDAO
from flask import jsonify
from config.validation import isDecomissioned



class BicycleHandler():

    def __init__(self):
        self.orderBy_attributes = ['bid', 'lp', 'rfid', 'bikestatus', 'model', 'brand']
        self.bike_attributes = ['bid', 'lp', 'rfid', 'bikestatus', 'model', 'brand', 'orderby']
        self.update_attributes = ['lp', 'bikestatus', 'rfid']

    def build_bike_dict(self, row):
        result = {}
        #result['bid'] = row[0]
        result['plate'] = row[1]
        result['rfid'] = row[2]
        result['status'] = row[3]
        result['model'] = row[4]
        result['brand'] = row[5]
        return result

    def build_arg_dict(self, row):
        result = {}
        result[row] = row[row]

    def getBicycle(self, form):
        bDao = BicycleDAO()

        filteredArgs = {}
        for arg in form:
            if form[arg] and arg in self.bike_attributes:
                if arg != 'orderby':
                    filteredArgs[arg] = form[arg]
                elif form[arg] in self.orderBy_attributes:
                    filteredArgs[arg] = form[arg]
        if len(filteredArgs) == 0:
            bike_list = bDao.getAllBicycles()

        else:
            if not 'orderby' in filteredArgs:
                bike_list = bDao.getBikeByArguments(filteredArgs)

            elif len(filteredArgs) == 1 and 'orderby' in filteredArgs:
                bike_list = bDao.getBikeWithSorting(filteredArgs['orderby'])
            else:
                bike_list = bDao.getBikeByArgumentsWithSorting(filteredArgs)

        result_list = []

        for row in bike_list:
            result = self.build_bike_dict(row)
            result_list.append(result)

        return jsonify(Inventory=result_list)

    def insert(self, form):
        plate = form['lp']
        rfid = form['rfid']
        model = form['model']
        brand = form['brand']

        if plate and rfid and model and brand:
            bDao = BicycleDAO()
            bID = bDao.insert(plate, rfid, model, brand)                                    #INSERT #1
            return jsonify("Bicycle was successfully added.")
        else:
            return jsonify(Error="Missing attributes of the bicycle."), 401

    def getBIDByRFID(self, rfid):
        bDao = BicycleDAO()
        bid = bDao.getBIDByRFID(rfid)
        return bid

    def getAvailableBicycleCount(self):
        bDao = BicycleDAO()
        count = bDao.getAvailableBicycleCount()
        return count

    def getStatusByID(self, bid):
        bDao = BicycleDAO()
        status = bDao.getStatusByID(bid)
        return status

    #@isDecomissioned
    def update(self, form):
        bDao = BicycleDAO()

        bid = form['bid']

        filteredArgs = {}
        for arg in form:
            if form[arg] and arg != 'bid' and arg in self.update_attributes:
                filteredArgs[arg] = form[arg]

        if len(filteredArgs) == 0:
            return jsonify(Error="No values given for update"), 400

        if not bid:
            return jsonify(Error="No bicycle id given")

        if not bDao.getBikeByID(bid):
            return jsonify(Error="Bicycle not found in inventory."), 401

        bDao.updateBicycle(filteredArgs, bid)                                               #UPDATE #1

        row = bDao.getBikeByID(bid)
        result = self.build_bike_dict(row)
        return jsonify(Bicycle=result), 200

    @isDecomissioned
    def updateStatusIsAvailable(self, bid, wid, rid):
        bDao = BicycleDAO()
        bDao.freeBicyle(bid, 'RENTED', wid, rid)                                                      #UPDATE #1

    @isDecomissioned
    def updateStatusIsReserved(self, bid, wid, rid):
        bDao = BicycleDAO()
        bDao.updateStatusCheckOut(bid, 'RENTED', wid, rid)                                                    #UPDATE #1

    def getBIDByPlate(self, plate):
        bDao = BicycleDAO()
        bid = bDao.getBIDByPlate(plate)
        return bid