from config.dbconfig import pg_config
import psycopg2

class BicycleDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def getAllBicycles(self):
        cursor = self.conn.cursor()
        query = "Select * From Bike"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBikeByArguments(self, args, kargs):
        cursor = self.conn.cursor()
        arguments = ""
        #values = list(args.values())
        for arg in args:
            arguments = arguments + arg + "= %s" + " and "
        arguments = arguments[:-5]  # Remove the last ' and '
        query = "Select * From Bike Where " + arguments
        cursor.execute(query, kargs)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBikeWithSorting(self, orderby):
        cursor = self.conn.cursor()
        query = "select * from Bike order by " + orderby
        cursor.execute(query)
        print(cursor.query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBikeByArgumentsWithSorting(self, args , kargs):
        cursor = self.conn.cursor()
        arguments = ""
        sort = kargs.pop(len(kargs) - 1)
        for arg in args:
            if arg != 'orderby':
                arguments = arguments + arg + "= %s" + " and "
        arguments = arguments[:-5]  # Remove the last ' and '
        query = "select * from Bike where " + arguments + " order by " + sort
        cursor.execute(query, kargs)
        print(cursor.query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBikeByID(self, bid):
        cur = self.conn.cursor()
        query = '''
                    Select *
                    From Bike
                    Where bid = %s
                '''
        cur.execute(query, (bid,))
        row = cur.fetchone()
        return row

    def getPlateByID(self, bid):
        cur = self.conn.cursor()
        query = '''
                    Select lp
                    From Bike
                    Where bid = %s
                '''
        cur.execute(query, (bid,))
        plate = cur.fetchone()
        return plate

    def getRFIDByID(self, bid):
        cur = self.conn.cursor()
        query = '''
                    Select rfid
                    From Bike
                    Where bid = %s
                '''
        cur.execute(query, (bid,))
        rfid = cur.fetchone()
        return rfid

    def getStatusByID(self, bid):
        cur = self.conn.cursor()
        query = '''
                    Select status
                    From Bike
                    Where bid = %s
                '''
        cur.execute(query, (bid,))
        status = cur.fetchone()
        return status

    def getModelByID(self, bid):
        cur = self.conn.cursor()
        query = '''
                    Select model
                    From Bike
                    Where bid = %s
                '''
        cur.execute(query, (bid,))
        model = cur.fetchone()
        return model

    def getBrandByID(self, bid):
        cur = self.conn.cursor()
        query = '''
                    Select brand
                    From Bike
                    Where bid = %s
                '''
        cur.execute(query, (bid,))
        brand = cur.fetchone()
        return brand

    def insert(self, plate, rfid, status, model, brand):
        cur = self.conn.cursor()
        query = '''
                    Insert into Bike(LP, RFID, Status, Model, Brand)
                    values (%s, %s, %s, %s, %s) returning bid
                '''
        cur.execute(query, (plate, rfid, status, model, brand,))
        bID = cur.fetchone()[0]
        self.conn.commit()
        return bID

    def updateBicycle(self, form, bid):
        argument = ""
        values = []
        for arg in form:
            argument = argument + arg + "= %s" + " And "
            value = form[arg]
            print(value)
            values.append(str(value))
        values.append(bid)
        argument = argument[:-5]
        print(argument)
        for arg in values:
            print(arg)
        query = '''Update Bike set ''' + argument + ''' Where BID = %s'''
        print(query)
        cur = self.conn.cursor()
        cur.execute(query, (values))
        self.conn.commit()


    def updatePlate(self, bid, plate):
        cur = self.conn.cursor()
        query = '''
                    Update Bike set lp = %s Where bid = %s 
                '''
        cur.execute(query, (plate, bid,))
        self.conn.commit()

    def updateRFID(self, bid, rfid):
        cur = self.conn.cursor()
        query = '''
                    Update Bike set rfid = %s Where bid = %s 
                '''
        cur.execute(query, (rfid, bid,))
        self.conn.commit()

    def updateStatus(self, bid, status):
        cur = self.conn.cursor()
        query = '''
                    Update Bike set status = %s Where bid = %s 
                '''
        cur.execute(query, (status, bid,))
        self.conn.commit()

    def updateModel(self, bid, model):
        cur = self.conn.cursor()
        query = '''
                    Update Bike set lp = %s Where bid = %s 
                '''
        cur.execute(query, (model, bid,))
        self.conn.commit()

    def updateBrand(self, bid, brand):
        cur = self.conn.cursor()
        query = '''
                    Update Bike set brand = %s Where bid = %s 
                '''
        cur.execute(query, (brand, bid,))
        self.conn.commit()

    def getBIDByRFID(self, rfid):
        cur = self.conn.cursor()
        query = '''
                    Select BID
                    From Bike
                    Where RFID = %s
                '''
        cur.execute(query, (rfid,))
        bid = cur.fetchone()
        return bid
