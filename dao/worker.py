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
            Select wID, status
            From Users natural inner join Worker
            Where email = %s and password = crypt(%s, password)
        '''
        cur.execute(query, (email, password))
        row = cur.fetchone()
        if row is None:
            return row

        return row

    def getWorkerByID(self, wid):
        cursor = self.conn.cursor()
        query = '''
            Select WID, FName, LName, Email, PNumber, Status
            From Users natural inner join Worker
            Where WID = %s
        '''
        cursor.execute(query, (wid,))
        result = cursor.fetchone()
        return result

    def getWorkerByUID(self, uid):
        cursor = self.conn.cursor()
        query = '''
            Select WID
            From Worker
            Where UID = %s
        '''
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        if result is None:
            return result
        wID = result[0]
        return wID

    def getWorkerByArguments(self, form):
        argument = ""
        values = []
        for arg in form:
            argument = argument + arg + "= %s" + " and "
            value = form[arg]
            values.append(str(value))
        argument = argument[:-5]
        cursor = self.conn.cursor()

        query = "Select WID, FName, LName, Email, PNumber, Status From Worker NATURAL INNER JOIN  Users Where " + argument
        cursor.execute(query, values)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getWorkerWithSorting(self, orderBy):
        cursor = self.conn.cursor()
        query = "select WID, FName, LName, Email, PNumber, Status from Worker NATURAL INNER JOIN Users order by " + orderBy
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getWorkerByArgumentsWithSorting(self, form):
        argument = ""
        values = []
        for arg in form:
            if arg != 'orderby':
                argument = argument + arg + "= %s" + " and "
                value = form[arg]
                values.append(str(value))
        argument = argument[:-5]
        cursor = self.conn.cursor()

        query = "select WID, FName, LName, Email, PNumber, Status from Worker NATURAL INNER JOIN Users where " + argument + " order by " + form['orderby']
        cursor.execute(query, values)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, uid):
        cursor = self.conn.cursor()
        query = '''
            insert into worker(UID, Status) values (%s, %s) returning wID
        '''
        cursor.execute(query, (uid, 'ACTIVE'))
        wID = cursor.fetchone()[0]
        self.conn.commit()
        return wID

    def updateStatus(self, wid, status):
        cursor = self.conn.cursor()
        query = '''
            update Worker set Status = %s Where WID = %s
            '''
        cursor.execute(query, (status, wid))
        self.conn.commit()

    def getAllWorkers(self):
        cursor = self.conn.cursor()
        query = '''SELECT WID, FName, LName, Email, PNumber, Status FROM Worker NATURAL INNER JOIN Users'''
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getWIDByEmail(self, email):
        cursor = self.conn.cursor()
        query = '''SELECT WID 
                    FROM Worker NATURAL INNER JOIN Users
                    Where email = %s
                    '''
        cursor.execute(query, email,)
        row = cursor.fetchone()
        if row is None:
            return row
        return row[0]




