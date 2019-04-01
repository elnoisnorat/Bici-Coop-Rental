from config.dbconfig import pg_config
import psycopg2

class MaintenanceDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def requestMaintenance(self, uid, bid, notes):
        cursor = self.conn.cursor()
        query = '''
          insert into Maintenance(StartTime, EndTime, Status, Notes, Bike, RequestedBy, ServicedBy)
          values (Null, Null, Queued, %s, %s, %s, Null) returning MID;
        '''
        cursor.execute(query, (notes, bid, uid))
        mID = cursor.fetchone()[0]
        self.conn.commit()
        return mID


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