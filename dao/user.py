import psycopg2
from config.dbconfig import pg_config

class UsersDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def insert(self, FName, LName, password, PNumber, Email):
        cursor = self.conn.cursor()
        query = '''
          insert into Users(FName, LName, password, PNumber, Email)
          values (%s, %s, crypt(%s, %s), %s, %s) returning uID;
        '''
        cursor.execute(query, (FName, LName, password, 'password', PNumber, Email,))
        uID = cursor.fetchone()[0]
        self.conn.commit()
        return uID

    def getUserByID(self, uid):
        cursor = self.conn.cursor()
        query = '''
            Select UID, FName, LName, Email, PNumber
            From Users
            Where UID = %s
        '''
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        return result

    def getUserByEmail(self, email):
        cursor = self.conn.cursor()
        query = '''
            Select UID, FName, LName, Email, PNumber
            From Users
            Where Email = %s
        '''
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result

    def updateName(self, email, fName, lName):
        cursor = self.conn.cursor()
        query = '''
            update Users set FName = %s, LName = %s
            Where Email = %s
        '''
        cursor.execute(query, (fName, lName, email,))
        result = cursor.fetchone()
        return result

    def updatePassword(self, email, password):
        cursor = self.conn.cursor()
        query = '''
            update Users set password = crypt(%s,  password)
            Where Email = %s
        '''
        cursor.execute(query, (password, email,))
        result = cursor.fetchone()
        return result

    def updatePNumber(self, email, pNumber):
        cursor = self.conn.cursor()
        query = '''
            update Users set PNumber = %s
            Where Email = %s
        '''
        cursor.execute(query, (pNumber, email,))
        result = cursor.fetchone()
        return result

    def getUserWithCID(self, cid):
        cursor = self.conn.cursor()
        query = '''
            Select UID, FName, LName, Email, PNumber
            From Users natural inner join Client
            Where CID = %s
        '''
        cursor.execute(query, (cid,))
        result = cursor.fetchone()
        return result

    def getUserIDByEmail(self, Email):
        cursor = self.conn.cursor()
        query = '''
            Select UID
            From Users
            Where Email = %s
        '''
        cursor.execute(query, (Email,))
        result = cursor.fetchone()
        return result

    def getUserWithWID(self, wid):
        cursor = self.conn.cursor()
        query = '''
            Select UID, FName, LName, Email, PNumber
            From Users natural inner join Worker
            Where WID = %s
        '''
        cursor.execute(query, (wid,))
        result = cursor.fetchone()
        return result