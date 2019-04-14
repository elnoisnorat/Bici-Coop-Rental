from config.dbconfig import pg_config
import psycopg2

class MaintenanceDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def requestMaintenance(self, uid, bid):
        try:
            cursor = self.conn.cursor()
            query = '''
            INSERT INTO Maintenance(starttime, status, bid, requestedby) 
            VALUES (now(), 'PENDING', %s, %s) 
            returning MID;
            '''
            cursor.execute(query, (bid, uid,))
            mID = cursor.fetchone()[0]

            query = '''
            Update Bike set status = 'MAINTENANCE' 
            Where BID = %s  
            '''
            cursor.execute(query, (bid,))

            self.conn.commit()
            return mID
        except Exception as e:
            self.conn.rollback()
            raise e


        '''
        MID SERIAL PRIMARY KEY,
        StartTime TIMESTAMP,
        EndTime TIMESTAMP,
        Status varchar(15),
        Notes VARCHAR(180),
        Bike INTEGER REFERENCES Bike(BID),
        RequestedBy INTEGER REFERENCES Worker(WID),
        ServicedBy INTEGER REFERENCES Worker(WID)
        '''

    def getMaintenance(self):
        cursor = self.conn.cursor()
        query = '''SELECT * FROM Maintenance Where endtime is Null'''
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def provideMaintenance(self, wid, mID, notes, service):
        try:
            cursor = self.conn.cursor()
            query = '''
            update Maintenance set EndTime = now(), ServicedBy = %s, notes = %s, Status = %s, Service = %s
            Where mID = %s and Status = 'PENDING'
            Returning BID
            '''
            cursor.execute(query, (wid, notes, 'FINISHED', service, mID))
            bid = cursor.fetchone()[0]
            query = '''
                        Update Bike set status = 'AVAILABLE' 
                        Where BID = %s  
                        '''
            cursor.execute(query, (bid,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def getRequestByBID(self, bid):
        cursor = self.conn.cursor()
        query = '''SELECT MID 
                   FROM Maintenance NATURAL INNER JOIN Bike 
                   Where BID = %s AND EndTime IS NULL
                '''
        cursor.execute(query, bid)
        result = cursor.fetchone()
        if result is None:
            return result
        mID = result[0]
        return mID

    def getRequestByMID(self, mid):
        cursor = self.conn.cursor()
        query = '''SELECT * 
                   FROM Maintenance
                   Where MID = %s
                '''
        cursor.execute(query, mid)
        result = cursor.fetchone()
        return result
