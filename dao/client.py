from config.dbconfig import pg_config
from flask import jsonify

import psycopg2

class ClientDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def clientLogin(self, email, password):
        cur = self.conn.cursor()
        query = '''
            Select CID
            From Users natural inner join Client
            Where email = %s and password = crypt(%s, password)
        '''
        cur.execute(query, (email, password))

        row = cur.fetchone()
        if row is None:
            return row
        return row[0]

    def insert(self, uID):
        cursor = self.conn.cursor()
        query = "insert into Client(UID) values (%s) returning CID"
        cursor.execute(query, (uID,))
        cID = cursor.fetchone()
        self.conn.commit()
        if cID is None:
            return cID
        return cID[0]

    def getClientByUID(self, uid):
        cursor = self.conn.cursor()
        query = '''
            Select *
            From Client
            Where UID = %s
        '''
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        return result

    def getClientByArguments(self, form):
        argument = ""
        values = []
        for arg in form:
            argument = argument + arg + "= %s" + " and "
            value = form[arg]
            values.append(str(value))
        argument = argument[:-5]
        cursor = self.conn.cursor()

        query = "Select CID, FName, LName, Email, PNumber, DebtorFlag " \
                "From Client NATURAL INNER JOIN Users Where " + argument
        cursor.execute(query, values)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getClientWithSorting(self, orderBy):
        cursor = self.conn.cursor()
        query = "select CID, FName, LName, Email, PNumber, DebtorFlag from Client NATURAL INNER JOIN Users order by " + orderBy
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getClientByArgumentsWithSorting(self, form):
        argument = ""
        values = []
        for arg in form:
            if arg != 'orderby':
                argument = argument + arg + "= %s" + " and "
                value = form[arg]
                values.append(str(value))
        argument = argument[:-5]
        cursor = self.conn.cursor()

        query = "select CID, FName, LName, Email, PNumber, DebtorFlag from Client NATURAL INNER JOIN Users where " + argument + " order by " + form['orderby']
        cursor.execute(query, values)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getClientByCID(self, cid):
        cursor = self.conn.cursor()
        query = '''
            Select *
            From Client
            Where CID = %s
        '''
        cursor.execute(query, (cid,))
        result = cursor.fetchone()
        return result

    def getAllClients(self):
        cursor = self.conn.cursor()
        query = '''SELECT CID, FName, LName, Email, PNumber, DebtorFlag 
                   from Client NATURAL INNER JOIN Users
                '''
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getCIDByUID(self, reqID):
        cursor = self.conn.cursor()
        query = '''
            Select CID
            From Client
            Where UID = %s
        '''
        cursor.execute(query, (reqID,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def getPhoneNumber(self, cid):
        cursor = self.conn.cursor()
        query = '''
                        Select pnumber
                        From Users natural inner join Client
                        Where CID = %s
                        '''
        cursor.execute(query, (cid,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def setDebtorFlag(self, cid):
        cursor = self.conn.cursor()
        query = '''
                update Client set debtorflag = True where cid= %s
                '''
        cursor.execute(query, (cid,))
        self.conn.commit()

    def getDebtorFlag(self, cid):
        cursor = self.conn.cursor()
        query = '''
                Select debtorflag
                From Client
                Where cid = %s
                '''
        cursor.execute(query, (cid,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def getName(self, cid):
        cursor = self.conn.cursor()
        query = '''
                        Select fname
                        From Client
                        Where cid = %s
                        '''
        cursor.execute(query, (cid,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]


