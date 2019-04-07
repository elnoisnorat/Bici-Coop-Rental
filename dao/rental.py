from config.dbconfig import pg_config
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

