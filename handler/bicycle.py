from dao.bicycle import BicycleDAO
from flask import jsonify
from config.validation import isDecomissioned



class BicycleHandler():

    def __init__(self):
        self.orderBy_attributes = ['bid', 'lp', 'rfid', 'bikestatus', 'model', 'brand', 'snumber']
        self.bike_attributes = ['bid', 'lp', 'rfid', 'bikestatus', 'model', 'brand', 'snumber', 'orderby']
        self.update_attributes = ['lp', 'bikestatus', 'rfid', 'brand', 'model']

    def build_bike_dict(self, row):
        result = {}
        result['bid'] = row[0]
        result['snumber'] = row[1]
        result['plate'] = row[2]
        result['rfid'] = row[3]
        result['status'] = row[4]
        result['brand'] = row[5]
        result['model'] = row[6]
        return result

    def build_arg_dict(self, row):
        result = {}
        result[row] = row[row]

    def getAllBicyclesInPhysicalInventory(self):
        bDao = BicycleDAO()
        result_list = bDao.getAllBicyclesInPhysicalInventory()
        bicycle_list = []
        for row in result_list:
            result = self.build_bike_dict(row)
            bicycle_list.append(result)
        return jsonify(Inventory=bicycle_list)


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
        try:
            plate = form['lp']
            rfid = form['rfid']
            model = form['model']
            brand = form['brand']
            snumber = form['snumber']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        if plate and rfid and model and brand and snumber:
            bDao = BicycleDAO()
            try:
                bID = bDao.insert(plate, rfid, model, brand, snumber)                                    #INSERT #1
                return jsonify("Bicycle was successfully added.")
            except Exception as e:
                return jsonify(Error="An error has occurred."), 400
        else:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

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
        try:
            bid = form['bid']
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        if not bid:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        filteredArgs = {}
        for arg in form:
            if form[arg] and arg != 'bid' and arg in self.update_attributes:
                filteredArgs[arg] = form[arg]

        if len(filteredArgs) == 0:
            return jsonify(Error="No values given for update request."), 400

        if not bDao.getBikeByID(bid):
            return jsonify(Error="A bicycle with the given arguments does not exist. "
                                 "Please verify the submitted arguments."), 400

        try:
            bDao.updateBicycle(filteredArgs, bid)                                               #UPDATE #1
        except Exception as e:
            return jsonify(Error="An error has occurred."), 400

        row = bDao.getBikeByID(bid)
        result = self.build_bike_dict(row)
        #return jsonify(Bicycle=result)
        return jsonify("Update was successful.")

    @isDecomissioned
    def updateStatusIsAvailable(self, bid, wid, rid):
        bDao = BicycleDAO()
        try:
            bDao.freeBicyle(bid, 'RENTED', wid, rid)                                                      #UPDATE #1
        except Exception as e:
            raise e

    @isDecomissioned
    def updateStatusIsReserved(self, bid, wid, rid):
        bDao = BicycleDAO()
        try:
            bDao.updateStatusCheckOut(bid, 'RENTED', wid, rid)                                                    #UPDATE #1
        except Exception as e:
            raise e

    def getBIDByPlate(self, plate):
        bDao = BicycleDAO()
        bid = bDao.getBIDByPlate(plate)
        return bid

    def swapStatus(self, newBID, rid):
        bDao = BicycleDAO()
        bid = bDao.swapStatus(newBID, rid)
        return bid

    def getBIDByRFIDForMaintenance(self, rfid):
        bDao = BicycleDAO()
        bid = bDao.getBIDByRFIDForMaintenance(rfid)
        return bid

    def getBIDByPlateForMaintenance(self, plate):
        bDao = BicycleDAO()
        bid = bDao.getBIDByPlateForMaintenance(plate)
        return bid

    def get_bicycle_for_swap(self, newRFID):
        bDao = BicycleDAO()
        bid = bDao.get_bicycle_for_swap(newRFID)
        return bid