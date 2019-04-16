from config.dbconfig import pg_config
import datetime
import psycopg2

class RentalDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def rentBicycle(self, cid, tid):  #NEEDS QUERY
        cursor = self.conn.cursor()
        query = '''
          INSERT INTO rental(stime, client, dueDate) 
          VALUES (now(), %s, now() +8 ) 
          RETURNING RID;
        '''
        cursor.execute(query, (cid,))
        rID = cursor.fetchone()[0]

        query = '''
            INSERT INTO RentLink(RID, TID) VALUES (%s, %s);
        '''
        cursor.execute(query, (rID, tid))

        self.conn.commit()
        return rID
        #return 1

    def getRentalByCID(self, cID): #ReceivedBy typo
        cursor = self.conn.cursor()
        query = '''
            Select *
            From Rental
            Where Client = %s AND ReceivedBy IS NULL
        '''
        cursor.execute(query, (cID,))

        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRentalByCIDCheckOut(self, cID): #ReceivedBy typo
        cursor = self.conn.cursor()
        query = '''
            Select *
            From Rental
            Where Client = %s AND ReceivedBy IS NULL AND DispatchedBy IS NULL
        '''
        cursor.execute(query, (cID,))

        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBIDByCID(self, cID):
        cursor = self.conn.cursor()
        query = '''
                Select BID
                From Rental
                Where Client = %s AND ReceivedBy IS NULL
                '''
        cursor.execute(query, (cID,))

        bid = cursor.fetchone()

        return bid

    def getRIDByBID(self, bid):
        cursor = self.conn.cursor()
        query = '''
                Select RID
                From Rental
                Where BID = %s and ETime IS NULL
                '''
        cursor.execute(query, (bid,))
        rid = cursor.fetchone()
        return rid

    def checkIn(self, wID, rid):
        debt = False
        try:
            cursor = self.conn.cursor()
            currenTime = datetime.datetime.now()
            query = '''
                    Update Rental set ReceivedBy = %s, ETime = %s Where RID = %s
                    returning duedate, client, bid
                '''
            cursor.execute(query, (wID, currenTime, rid,))
            row = cursor.fetchone()
            dueDate = row[0]
            client = row[1]
            bid = row[2]

            query = '''
                    Update Bike set bikestatus = %s Where BID = %s
                    '''
            cursor.execute(query, ('AVAILABLE', bid,))

            if currenTime > dueDate:
                debt = True
                query = '''
                Update Client set debtorflag = %s Where CID = %s
                '''
                cursor.execute(query, (True, client,))
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            raise e
        return debt

    def getRentalByID(self, rid):
        cursor = self.conn.cursor()
        query = '''
                Select *
                From Rental
                Where RID = %s
                '''
        cursor.execute(query, (rid,))
        result = cursor.fetchone()
        return result

    def checkOut(self, wID, bid, rid):
        cur = self.conn.cursor()
        query = '''
                    Update Rental set DispatchedBy = %s, BID = %s, STime = CURRENT_DATE Where RID = %s
                '''
        cur.execute(query, (wID, bid, rid,))
        self.conn.commit()

    def getBIDByCIDAndPlate(self, cid, plate):
        cursor = self.conn.cursor()
        query = '''
            Select BID
            From Rental Natural Inner Join Bike
            Where Client = %s AND lp = %s AND ReceivedBy IS NULL
        '''
        cursor.execute(query, (cid, plate,))
        result = cursor.fetchone()
        if result is None:
            return result
        bid = result[0]

        return bid

    def getNewRentals(self, tid):
        cursor = self.conn.cursor()
        query = '''
            Select RID
            From RentLink NATURAL INNER JOIN Rental
            Where TID = %s
        '''
        cursor.execute(query, (tid,))
        result = []
        for row in cursor:
            result.append(row)

        return result

