from config.dbconfig import pg_config
import psycopg2

class RentalDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def rentBicycle(self,cid,tid):  #NEEDS QUERY
        #cursor = self.conn.cursor()
        #query = '''
        #  insert into Rental(CID, TID, STime, ETime, BID, ReceivedBy, DispatchedBy)
        #  values (%s, %s, NOW(), Null, Null , Null, Null) returning rID;
        #'''
        #cursor.execute(query, (cid, tid,))
        #rID = cursor.fetchone()[0]
        #self.conn.commit()
        #return rID
        return 1

    def getRentalByCID(self, cID): #ReceivedBy typo
        cursor = self.conn.cursor()
        query = '''
            Select *
            From Rental
            Where Client = %s AND RecivedBy IS NULL
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
                Where Client = %s AND RecivedBy IS NULL
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
        cur = self.conn.cursor()
        query = '''
                    Update Rental set RecivedBy = %s AND ETime = CURRENT_DATE Where RID = %s
                '''
        cur.execute(query, (wID, rid,))
        self.conn.commit()
        return rid

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
                    Update Rental set DispatchedBy = %s AND BID = %s AND STime = CURRENT_DATE Where RID = %s
                '''
        cur.execute(query, (wID, bid, rid,))
        self.conn.commit()

    def editPlan(self, name, amount):
        cur = self.conn.cursor()
        query =" UPDATE Plans set name = %s, amount = %s WHERE PID = 1"
        cur.execute(query, (name, amount))
        #print(cur.fetchone())
        self.conn.commit()

    def editOverduePlan(self, name,amount):
        cur = self.conn.cursor()
        query = " UPDATE Plans set name = %s, amount = %s WHERE PID = 2"
        cur.execute(query, (name, amount))
        self.conn.commit()

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





