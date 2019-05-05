from config.dbconfig import pg_config
import datetime
import psycopg2

class RentalDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    # def rentBicycle(self, cid, tid):  #NEEDS QUERY
    #     cursor = self.conn.cursor()
    #     query = '''
    #       INSERT INTO rental(stime, client, dueDate)
    #       VALUES (now(), %s, now() +8 )
    #       RETURNING RID;
    #     '''
    #     cursor.execute(query, (cid,))
    #     rID = cursor.fetchone()[0]
    #
    #     query = '''
    #         INSERT INTO RentLink(RID, TID) VALUES (%s, %s);
    #     '''
    #     cursor.execute(query, (rID, tid))
    #
    #     self.conn.commit()
    #     return rID

    def getRentalByCID(self, cID): #ReceivedBy typo
        cursor = self.conn.cursor()
        query = '''
            Select rid, stime, etime, duedate, bid 
            From Rental
            Where Client = %s AND ReceivedBy IS NULL AND etime IS NULL
        '''
        cursor.execute(query, (cID,))

        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRentalAmountByCID(self, cID): #ReceivedBy typo
        cursor = self.conn.cursor()
        query = '''
            Select count(*)
            From Rental
            Where Client = %s AND ReceivedBy IS NULL AND etime is NULL
        '''
        cursor.execute(query, (cID,))

        result = cursor.fetchone()[0]
        return result

    def getRentalByCIDCheckOut(self, cID): #ReceivedBy typo
        cursor = self.conn.cursor()
        query = '''
            Select *
            From Rental
            Where Client = %s AND ReceivedBy IS NULL AND DispatchedBy IS NULL AND etime IS NULL
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
                Where Client = %s AND ReceivedBy IS NULL AND etime IS NULL
                '''
        cursor.execute(query, (cID,))

        bid = cursor.fetchone()
        if bid is None:
            return bid
        return bid[0]

    def getRIDByBID(self, bid):
        cursor = self.conn.cursor()
        query = '''
                Select RID
                From Rental
                Where BID = %s and ETime IS NULL
                '''
        cursor.execute(query, (bid,))
        rid = cursor.fetchone()
        if rid is None:
            return rid
        return rid[0]

    def checkIn(self, wID, rid):
        debt = False
        try:
            cursor = self.conn.cursor()
            #currentTime = datetime.datetime.now()
            query = '''
                    Update Rental set ReceivedBy = %s, ETime = now() Where RID = %s
                    returning duedate, client, bid, ETime
                '''
            cursor.execute(query, (wID, rid,))
            row = cursor.fetchone()
            dueDate = row[0]
            client = row[1]
            bid = row[2]
            eTime = row[3]

            query = '''
                    Update Bike set bikestatus = %s Where BID = %s
                    '''
            cursor.execute(query, ('AVAILABLE', bid,))

            if eTime > dueDate:
                debt = True
                # query = '''
                # Update Client set debtorflag = %s Where CID = %s
                # '''
                # cursor.execute(query, (True, client,))
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
                    Update Rental set DispatchedBy = %s, BID = %s, STime = now() Where RID = %s
                '''
        cur.execute(query, (wID, bid, rid,))
        self.conn.commit()

    def getBIDByCIDAndPlate(self, cid, plate):
        cursor = self.conn.cursor()
        query = '''
            Select BID
            From Rental Natural Inner Join Bike
            Where Client = %s AND lp = %s AND ReceivedBy IS NULL AND etime IS NULL
        '''
        cursor.execute(query, (cid, plate,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def getNewRentals(self, tid, payment):
        cursor = self.conn.cursor()
        if payment == 'CASH':
            query = '''
            Select RID, stime + INTERVAL '3 hour', duedate
            From RentLink NATURAL INNER JOIN Rental
            Where TID = %s
        '''
        elif payment == 'CARD':
            query = '''
                        Select RID, duedate, duedate + INTERVAL '5 minute'
                        From RentLink NATURAL INNER JOIN Rental
                        Where TID = %s
                    '''
        cursor.execute(query, (tid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_rental_by_rid_and_rfid(self, rid, oldRFID):
        cursor = self.conn.cursor()
        query = '''
                    Select BID
                    From Rental NATURAL INNER JOIN Bike
                    Where RID = %s and RFID = %s and bikestatus = 'MAINTENANCE'
                '''
        cursor.execute(query, (rid, oldRFID,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def getPlan(self):
        cur = self.conn.cursor()
        query = " Select name, amount from plans WHERE PID = 1"
        cur.execute(query)
        result = cur.fetchone()
        return result

    def getOverduePlan(self):
        cur = self.conn.cursor()
        query = " Select name, amount from plans WHERE PID = 2"
        cur.execute(query)
        print("Query:\n")
        result = cur.fetchone()
        print(result[0][0])
        return result

    def getClientByRID(self, rid):
        cur = self.conn.cursor()
        query = " Select client From Rental Where RID = %s"
        cur.execute(query, (rid,))
        result = cur.fetchone()
        if result is None:
            return result
        return result[0]

    def isLate(self, rid):
        cur = self.conn.cursor()
        query = " Select client From Rental Where RID = %s and duedate < now()"
        cur.execute(query, (rid,))
        result = cur.fetchone()
        if result is None:
            return result
        return result[0]

    def wasDispatched(self, rid):
        cur = self.conn.cursor()
        query = " Select DispatchedBy From Rental Where RID = %s"
        cur.execute(query, (rid,))
        result = cur.fetchone()
        if result is None:
            try:
                query = "UPDATE Rental set etime = now() Where RID = %s"
                cur.execute(query, (rid,))
                query = '''
                  UPDATE bike SET bikestatus = 'AVAILABLE'
                  WHERE BID in (SELECT bid from bike 
                                where bikestatus = 'RESERVED' limit 1) 
                                returning bid
                        '''
                cur.execute(query)
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                raise e

    def getStripeToken(self, rid):
        cursor = self.conn.cursor()
        query = "SELECT token " \
                "From Transactions natural inner join RentLink natural inner join Rental" \
                "Where rid = %s"
        cursor.execute(query, (rid,))
        result = cursor.fetchone()[0]
        return result
