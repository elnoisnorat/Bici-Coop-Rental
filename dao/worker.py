import psycopg2
from config.dbconfig import pg_config
from config.encryption import SECRET_KEY
class WorkerDAO:
    def __init__(self):
        self.conn = psycopg2._connect(pg_config['connection_url'])

    def workerLogin(self, email, password):
        cur = self.conn.cursor()
        # query = ''' Select wID, status
        #     From Users natural inner join Worker
        #     Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s and password = crypt(%s, password) '''
        query ='''
            Select wID, status
            From Users natural inner join Worker
            Where email = %s and password = crypt(%s, password)
        '''
        # cur.execute(query, (SECRET_KEY, email, password, ) )
        cur.execute(query, (email, password))
        row = cur.fetchone()
        if row is None:
            return row
        return row

    def getWorkerByID(self, wid):
        cursor = self.conn.cursor()
        # query = '''select  WID,
        #                                                              PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
        #                                                              PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
        #                                                              PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
        #                                                              PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber,
        #                                                              Status
        #                                                              from Users NATURAL INNER JOIN Worker WID = %s and confirmation = %s;
        #
        #                                                              '''
        query = '''
            Select WID, FName, LName, Email, PNumber, Status
            From Users natural inner join Worker
            Where WID = %s and confirmation = %s
        '''
        #cursor.execute(query, (SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY, wid, True,))
        cursor.execute(query, (wid, True,))
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
        # query = '''select  WID,
        #                                                                      PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
        #                                                                      PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
        #                                                                      PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
        #                                                                      PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber,
        #                                                                      Status
        #                                                                      from Users NATURAL INNER JOIN Worker;
        #
        #                                                                      '''
        query = '''SELECT WID, FName, LName, Email, PNumber, Status FROM Worker NATURAL INNER JOIN Users'''
        # cursor.execute(query, (SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY,))
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getWIDByEmail(self, email):
        cursor = self.conn.cursor()
        # query = '''SELECT WID
        #             FROM Worker NATURAL INNER JOIN Users
        #             Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s '''
        query = '''SELECT WID 
                    FROM Worker NATURAL INNER JOIN Users
                    Where Email = %s
                    '''
        #cursor.execute(query, (SECRET_KEY, email,))
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        if row is None:
            return row
        return row[0]

    def getWorkerForMaintenance(self, email):
        cursor = self.conn.cursor()
        # query = '''SELECT WID
        #                     FROM Worker NATURAL INNER JOIN Users
        #                     Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s and status = 'ACTIVE' and confirmation = %s
        #                     '''
        query = '''SELECT WID 
                    FROM Worker NATURAL INNER JOIN Users
                    Where Email = %s and status = 'ACTIVE' and confirmation = %s
                    '''
        #cursor.execute(query, (SECRET_KEY, email, True))
        cursor.execute(query, (email, True))
        row = cursor.fetchone()
        if row is None:
            return row
        return row[0]

    def getConfirmedWorker(self):
        cursor = self.conn.cursor()
        # query = query = '''select  WID,
        #                                                                      PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
        #                                                                      PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
        #                                                                      PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
        #                                                                      PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber,
        #                                                                      Status
        #                                                                      from Users NATURAL INNER JOIN Worker;'''
        query = '''SELECT WID, FName, LName, Email, PNumber, Status 
                    FROM Worker NATURAL INNER JOIN Users
                    Where confirmation = %s
                    '''
        # cursor.execute(query, (SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY, True, ))
        cursor.execute(query, (True,))
        result = []
        for row in cursor:
            result.append(row)
        return result




