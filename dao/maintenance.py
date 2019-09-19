from config.dbconfig import pg_config
import psycopg2

class MaintenanceDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s sslmode=%s sslrootcert=%s" % (
            pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'],
            pg_config['mode'], pg_config['cert'])
        self.conn = psycopg2._connect(connection_url)
        # self.conn = psycopg2._connect(pg_config['connection_url'])
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
                   Where MID = %s and status = 'PENDING'
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

    def provideMaintenance(self, wid, mID, notes):
        release = 0
        try:
            cursor = self.conn.cursor()
            query = '''
                Select BID
                From Maintenance
                Where MID = %s and Status = %s
            '''
            cursor.execute(query, (mID, 'PENDING'))

            swap = cursor.fetchone()

            if swap is None:
                return swap
            bid = swap[0]

            size = len(self.getRequestByBID(bid))
            if size == 1:
                query = '''
                            Select RID
                            From Rental
                            Where BID = %s and ETime IS NULL
                        '''
                cursor.execute(query, (bid,))
                rental = cursor.fetchone()
                if rental is None:
                    query = '''
                            Update Bike set bikestatus = 'AVAILABLE' 
                            Where BID = %s  
                            '''
                else:
                    query = '''
                        Update Bike set bikestatus = 'RENTED' 
                        Where BID = %s  
                        '''
                    release = 1
                cursor.execute(query, (bid,))

            query = '''
            update Maintenance set EndTime = now(), ServicedBy = %s, notes = %s, Status = %s
            Where mID = %s and Status = %s
            '''
            cursor.execute(query, (wid, notes, 'FINISHED', mID, 'PENDING'))
            self.conn.commit()
            return release
        except Exception as e:
            self.conn.rollback()
            raise e

    def provideMaintenancePlate(self, wid, mID, notes, plate):
        release = 0
        try:
            cursor = self.conn.cursor()
            query = '''
                        Select BID
                        From Maintenance
                        Where MID = %s and Status = %s
                    '''
            cursor.execute(query, (mID, 'PENDING'))

            swap = cursor.fetchone()

            if swap is None:
                return swap
            bid = swap[0]

            query = '''
                UPDATE Bike set lp = %s
                Where BID = %s
            '''
            cursor.execute(query, (plate, bid,))

            size = len(self.getRequestByBID(bid))
            if size == 1:
                query = '''
                                    Select RID
                                    From Rental
                                    Where BID = %s and ETime IS NULL
                                '''
                cursor.execute(query, (bid,))
                rental = cursor.fetchone()
                if rental is None:
                    query = '''
                                    Update Bike set bikestatus = 'AVAILABLE' 
                                    Where BID = %s  
                                    '''
                else:
                    query = '''
                                Update Bike set bikestatus = 'RENTED' 
                                Where BID = %s  
                                '''
                    release = 1
                cursor.execute(query, (bid,))

            query = '''
                    update Maintenance set EndTime = now(), ServicedBy = %s, notes = %s, Status = %s
                    Where mID = %s and Status = %s
                    '''
            cursor.execute(query, (wid, notes, 'FINISHED', mID, 'PENDING'))
            self.conn.commit()
            return release
        except Exception as e:
            self.conn.rollback()
            raise e

    def provideMaintenanceRFID(self, wid, mID, notes, rfid):
        release = 0
        try:
            cursor = self.conn.cursor()
            query = '''
                        Select BID
                        From Maintenance
                        Where MID = %s and Status = %s
                    '''
            cursor.execute(query, (mID, 'PENDING'))

            swap = cursor.fetchone()

            if swap is None:
                return swap
            bid = swap[0]

            query = '''
                UPDATE Bike set rfid = %s
                Where BID = %s
            '''
            cursor.execute(query, (rfid, bid,))

            size = len(self.getRequestByBID(bid))
            if size == 1:
                query = '''
                                    Select RID
                                    From Rental
                                    Where BID = %s and ETime IS NULL
                                '''
                cursor.execute(query, (bid,))
                rental = cursor.fetchone()
                if rental is None:
                    query = '''
                                    Update Bike set bikestatus = 'AVAILABLE' 
                                    Where BID = %s  
                                    '''
                else:
                    query = '''
                                Update Bike set bikestatus = 'RENTED' 
                                Where BID = %s  
                                '''
                    release = 1
                cursor.execute(query, (bid,))

            query = '''
                    update Maintenance set EndTime = now(), ServicedBy = %s, notes = %s, Status = %s
                    Where mID = %s and Status = %s
                    '''
            cursor.execute(query, (wid, notes, 'FINISHED', mID, 'PENDING'))
            self.conn.commit()
            return release
        except Exception as e:
            self.conn.rollback()
            raise e
