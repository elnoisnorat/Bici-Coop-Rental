from config.dbconfig import pg_config
import psycopg2

class ServiceMaintenanceDAO:

    def __init__(self):
        self.conn = psycopg2._connect(pg_config['connection_url'])

    def requestServiceMaintenance(self, uid, uName, uLName, service, price, notes):
        cursor = self.conn.cursor()
        query = '''
          insert into ServiceMaintenance(FName, LName, Bike, Service, Price, WorkedBy, WorkStatus, Notes, STime, ETime)
          values (%s, %s, %s, %s, %s, Null, Queued, %s, Null, Null) returning SMID;
        '''
        cursor.execute(query, (uid, uName, uLName, service, price, notes))
        mID = cursor.fetchone()
        self.conn.commit()
        if mID is None:
            return mID
        return mID[0]

    '''
        SMID SERIAL PRIMARY KEY, 
        FName varchar(50), 
        LName varchar(50), 
        Bike varchar(50), 
        Service varchar(100), 
        Price REAL, 
        WorkedBy INTEGER REFERENCES Worker(WID), 
        WorkStatus varchar(15), 
        Notes VARCHAR(180), 
        STime TIMESTAMP, 
        ETime TIMESTAMP
    '''