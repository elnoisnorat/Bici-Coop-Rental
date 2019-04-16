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

    def getBikeByArguments(self, form):
        argument = ""
        values = []
        for arg in form:
            argument = argument + arg + "= %s" + " and "
            value = form[arg]
            values.append(str(value))
        argument = argument[:-5]
        cursor = self.conn.cursor()

        query = "Select * From Bike Where " + argument

        cursor.execute(query, values)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBikeWithSorting(self, orderBy):
        cursor = self.conn.cursor()
        query = "select * from Bike order by " + orderBy
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBikeByArgumentsWithSorting(self, form):
        argument = ""
        values = []
        for arg in form:
            if arg != 'orderby':
                argument = argument + arg + "= %s" + " and "
                value = form[arg]
                values.append(str(value))
        argument = argument[:-5]
        cursor = self.conn.cursor()

        query = "select * from Bike where " + argument + " order by " + form['orderby']
        cursor.execute(query, values)
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
                    Where bid = %s and Status != %s
                '''
        cur.execute(query, (bid, 'DECOMMISSIONED'))
        rfid = cur.fetchone()[0]
        return rfid

    def getStatusByID(self, bid):
        cur = self.conn.cursor()
        query = '''
                    Select status
                    From Bike
                    Where bid = %s
                '''
        cur.execute(query, (bid,))
        status = cur.fetchone()[0]
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
            argument = argument + arg + "= %s" + ", "
            value = form[arg]
            values.append(str(value))
        values.append(bid)
        argument = argument[:-2]
        query = '''Update Bike set ''' + argument + ''' Where BID = %s'''
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
                    Where RFID = %s and bikestatus != %s
                '''
        cur.execute(query, (rfid, 'DECOMMISSIONED'))
        bid = cur.fetchone()[0]
        return bid

    def getAvailableBicycleCount(self):
        cur = self.conn.cursor()
        query = '''
                    Select count(*)
                    From Bike
                    Where bikestatus = %s
                '''
        cur.execute(query, ('AVAILABLE',))
        count = cur.fetchone()[0]
        return count

    def updateStatusCheckOut(self, bid, status, wid, rid):
        try:
            cur = self.conn.cursor()
            query = '''
                    Update Bike set bikestatus = %s Where bid = %s 
                '''
            cur.execute(query, (status, bid,))
            query = '''
                    Update Rental set DispatchedBy = %s, BID = %s, STime = CURRENT_DATE Where RID = %s
                    '''
            cur.execute(query, (wid, bid, rid,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def freeBicyle(self, bid, status, wid, rid):
        try:
            cur = self.conn.cursor()
            query = '''
                    Update Bike set bikestatus = %s Where bid = %s 
                '''
            cur.execute(query, (status, bid,))

            query = '''
                    UPDATE Bike set bikestatus = 'AVAILABLE' 
                    where bid = (SELECT BID from bike 
                                  where bikestatus= 'RESERVED' LIMIT 1);
                '''
            cur.execute(query)

            query = '''
                    Update Rental 
                    set DispatchedBy = %s, BID = %s, STime = CURRENT_DATE 
                    Where RID = %s
                     '''
            cur.execute(query, (wid, bid, rid,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def getBIDByPlate(self, plate):
        cur = self.conn.cursor()
        query = '''
                    Select BID
                    From Bike
                    Where lp = %s
                '''
        cur.execute(query, (plate,))
        plate = cur.fetchone()[0]
        return plate