from config.dbconfig import pg_config
import psycopg2

class MaintenanceDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def requestMaintenance(self, uid, bid, service_list):
        try:
            cursor = self.conn.cursor()
            for service in service_list:
                query = '''
                  INSERT INTO Maintenance(starttime, status, bid, requestedby, service) 
                  VALUES (now(), 'PENDING', %s, %s, %s) 
                  returning MID;
                  '''
                cursor.execute(query, (bid, uid, service,))

            query = '''
            Update Bike set bikestatus = 'MAINTENANCE' 
            Where BID = %s  
            '''
            cursor.execute(query, (bid,))

            self.conn.commit()
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
        query = '''SELECT MID, starttime, Status, bid, lp, bikestatus, service, brand, model
                    FROM Maintenance Natural Inner join Bike 
                    Where endtime is Null
                    Order by starttime
                    '''
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def provideMaintenance(self, wid, mID, notes, role):
        try:
            cursor = self.conn.cursor()
            query = '''
            update Maintenance set EndTime = now(), ServicedBy = %s, notes = %s, Status = %s
            Where mID = %s and Status = %s
            Returning BID
            '''
            cursor.execute(query, (wid, notes, 'FINISHED', mID, 'PENDING'))
            expected_bid = cursor.fetchone()
            if expected_bid is None:
                return expected_bid

            bid = expected_bid[0]

            size = len(self.getRequestByBID(bid))

            if size == 0:
                if role == 'Worker':
                    query = '''
                          Update Bike set bikestatus = 'AVAILABLE' 
                          Where BID = %s  
                          '''
                elif role == 'Client':
                    query = '''
                          Update Bike set bikestatus = 'RENTED' 
                          Where BID = %s  
                          '''
                cursor.execute(query, (bid,))
            self.conn.commit()
            return size
        except Exception as e:
            self.conn.rollback()
            raise e

    # def provideMaintenanceReturningPNumber(self, wid, mID, notes, service):
    #     try:
    #         cursor = self.conn.cursor()
    #         query = '''
    #         update Maintenance set EndTime = now(), ServicedBy = %s, notes = %s, Status = %s, Service = %s
    #         Where mID = %s and Status = 'PENDING'
    #         Returning BID
    #         '''
    #         cursor.execute(query, (wid, notes, 'FINISHED', service, mID))
    #         bid = cursor.fetchone()[0]
    #         query = '''
    #                     Update Bike set bikestatus = 'RENTED'
    #                     Where BID = %s
    #                     '''
    #         cursor.execute(query, (bid,))
    #         self.conn.commit()
    #     except Exception as e:
    #         self.conn.rollback()
    #         raise e

    def getRequestByBID(self, bid):
        cursor = self.conn.cursor()
        query = '''SELECT Service
                   FROM Maintenance NATURAL INNER JOIN Bike 
                   Where BID = %s AND EndTime IS NULL
                '''
        cursor.execute(query, (str(bid),))
        service_list = []
        for row in cursor:
            service_list.append(row[0])
        return service_list

    def getRequestByMID(self, mid):
        cursor = self.conn.cursor()
        query = '''SELECT * 
                   FROM Maintenance
                   Where MID = %s
                '''
        cursor.execute(query, mid)
        result = cursor.fetchone()
        return result

    def getRequestedByWithMID(self, mid):
        cursor = self.conn.cursor()
        query = '''SELECT requestedby 
                   FROM Maintenance
                   Where MID = %s
                '''
        cursor.execute(query, (mid,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def getService(self, mid):
        cursor = self.conn.cursor()
        query = '''SELECT Service 
                   FROM Maintenance
                   Where MID = %s
                '''
        cursor.execute(query, (mid,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def provideMaintenancePlate(self, wid, mID, notes, role, plate):
        try:
            cursor = self.conn.cursor()
            query = '''
                UPDATE Bike set lp = %s
            '''
            cursor.execute(query, (plate,))

            query = '''
            update Maintenance set EndTime = now(), ServicedBy = %s, notes = %s, Status = %s
            Where mID = %s and Status = %s
            Returning BID
            '''
            cursor.execute(query, (wid, notes, 'FINISHED', mID, 'PENDING'))
            expected_bid = cursor.fetchone()
            if expected_bid is None:
                return expected_bid

            bid = expected_bid[0]

            size = len(self.getRequestByBID(bid))

            if size == 0:
                if role == 'Worker':
                    query = '''
                          Update Bike set bikestatus = 'AVAILABLE' 
                          Where BID = %s  
                          '''
                elif role == 'Client':
                    query = '''
                          Update Bike set bikestatus = 'RENTED' 
                          Where BID = %s  
                          '''
                cursor.execute(query, (bid,))
            self.conn.commit()
            return size
        except Exception as e:
            self.conn.rollback()
            raise e

    def provideMaintenanceRFID(self, wid, mid, notes, role, rfid):
        try:
            cursor = self.conn.cursor()

            query = '''
                UPDATE Bike set rfid = %s
            '''
            cursor.execute(query, (rfid,))

            query = '''
            update Maintenance set EndTime = now(), ServicedBy = %s, notes = %s, Status = %s
            Where mID = %s and Status = %s
            Returning BID
            '''
            cursor.execute(query, (wid, notes, 'FINISHED', mID, 'PENDING'))
            expected_bid = cursor.fetchone()
            if expected_bid is None:
                return expected_bid

            bid = expected_bid[0]

            size = len(self.getRequestByBID(bid))

            if size == 0:
                if role == 'Worker':
                    query = '''
                          Update Bike set bikestatus = 'AVAILABLE' 
                          Where BID = %s  
                          '''
                elif role == 'Client':
                    query = '''
                          Update Bike set bikestatus = 'RENTED' 
                          Where BID = %s  
                          '''
                cursor.execute(query, (bid,))
            self.conn.commit()
            return size
        except Exception as e:
            self.conn.rollback()
            raise e
