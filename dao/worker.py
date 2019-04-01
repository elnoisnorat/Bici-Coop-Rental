import psycopg2
from config.dbconfig import pg_config
class WorkerDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def workerLogin(self, email, password):
        cur = self.conn.cursor()
        query ='''
            Select wID
            From Users natural inner join Worker
            Where email = %s and password = crypt(%s, password)
        '''
        cur.execute(query, (email, password))
        wID = cur.fetchone()
        return wID

    def getWorkerByID(self, wid):
        cursor = self.conn.cursor()
        query = '''
            Select WID, FName, LName, Status
            From Users natural inner join Worker
            Where WID = %s
        '''
        cursor.execute(query, (wid,))
        result = cursor.fetchone()
        return result

    def getWorkerByUID(self):
        return ''

    def getWorkerByArguments(self):
        return ''

    def getWorkerWithSorting(self):
        return ''

    def getWorkerByArgumentsWithSorting(self):
        return ''

    def insert(self, uid, status):
        cursor = self.conn.cursor()
        query = '''
            insert into worker(UID, Status) values (%s, %s) returning wID
        '''
        cursor.execute(query, (uid, status))
        wID = cursor.fetchone()[0]
        self.conn.commit()
        return wID

    def updateStatus(self, wid, status):
        cursor = self.conn.cursor()
        query = '''
            update Worker set Status = %s Where WID = %s
            '''
        cursor.execute(query, (wid, status))
        self.conn.commit()



