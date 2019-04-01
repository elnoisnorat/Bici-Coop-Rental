from dao.bicycle import BicycleDAO
from flask import jsonify


class BicycleHandler():

    def __init__(self):
        self.bike_attributes = ['bid', 'lp', 'rfid', 'status', 'model', 'brand', 'orderby']

    def build_bike_dict(self, row):
        result = {}
        result['bid'] = row[0]
        result['plate'] = row[1]
        result['rfid'] = row[2]
        result['status'] = row[3]
        result['model'] = row[4]
        result['brand'] = row[5]
        return result

    def build_arg_dict(self, row):
        result = {}
        result[row] = row[row]

    def getBicycle(self, args):
        bDao = BicycleDAO()

        argName = []
        argValue = []

        for arg in args:
            if args[arg] and arg in self.bike_attributes:
                argName.append(arg)
                argValue.append(args[arg])

        if len(argName) == 0:
            bike_list = bDao.getAllBicycles()
        else:
            '''
            for arg in args:
                if not arg in self.bike_attributes:
                    return jsonify(Error="Invalid Argument"), 401
            '''
            if not 'orderby' in argName:
                bike_list = bDao.getBikeByArguments(argName, argValue)

            elif ((len(argName)) == 1) and 'orderby' in argName:
                bike_list = bDao.getBikeWithSorting(argValue[0])

            else:
                bike_list = bDao.getBikeByArgumentsWithSorting(argName, argValue)

        result_list = []

        for row in bike_list:
            result = self.build_bike_dict(row)
            result_list.append(result)

        return jsonify(Inventory=result_list)

    def insert(self, form):
        plate = form['lp']
        rfid = form['rfid']
        status = form['status']
        model = form['model']
        brand = form['brand']

        if plate and rfid and status and model and brand:
            bDao = BicycleDAO()
            bID = bDao.insert(plate, rfid, status, model, brand)
            print(bID)
            return jsonify("Bicycle was successfully added.")
        else:
            return jsonify(Error="Missing attributes of the bicycle."), 401

    def update(self, form):
        bDao = BicycleDAO()

        bid = form['bid']

        filteredArgs = {}
        for arg in form:
            if form[arg] and arg != 'bid' and arg in self.bike_attributes:
                filteredArgs[arg] = form[arg]

        if len(filteredArgs) == 0:
            return jsonify(Error="No values given for update"), 400

        if not bid:
            return jsonify(Error="No bicycle id given")

        if not bDao.getBikeByID(bid):
            return jsonify(Error="Bicycle not found in inventory."), 401

        bDao.updateBicycle(filteredArgs, bid)

        row = bDao.getBikeByID(bid)
        result = self.build_bike_dict(row)
        return jsonify(Bicycle=result), 200

    def getBIDByRFID(self, rfid):
        bDao = BicycleDAO()
        bid = bDao.getBIDByRFID(rfid)
        return bid

