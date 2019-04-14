import psycopg2
from werkzeug.security import gen_salt

from config.dbconfig import pg_config
import datetime

from handler.sendEmail import EmailHandler


class UsersDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def insert(self, FName, LName, password, PNumber, Email, Role):
        try:
            cursor = self.conn.cursor()
            query = '''
                  insert into Users(FName, LName, password, PNumber, Email, confirmation, blocked, logattempt)
                  values (%s, %s, crypt(%s, gen_salt('bf')), %s, %s, %s, %s, %s) returning uID;
                  '''
            cursor.execute(query,
                       (FName, LName, password, PNumber, Email, False, datetime.datetime.now(), 0))
            uID = cursor.fetchone()[0]
            # self.conn.commit()
            # return uID
            if Role == "Client":
                query = "insert into Client(UID, debtorflag) values (%s, FALSE)"

            if Role == "Admin":
                query = "insert into Admin(UID) values (%s)"

            if Role == "Worker":
                query = "insert into Worker(UID, Status) values (%s, 'Active')"

            cursor.execute(query, (uID,))
            #cID = cursor.fetchone()
            #EmailHandler().confirmationEmail(Email, uID)

            self.conn.commit()
            pass
        except Exception as e:
            self.conn.rollback()
            raise e
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
            update Users set password = crypt(%s,  gen_salt('bf'))
            Where Email = %s
            returning UID
        '''
        cursor.execute(query, (password, email,))
        result = cursor.fetchone()[0]
        self.conn.commit()
        return result

    def updatePNumber(self, email, pNumber):
        cursor = self.conn.cursor()
        query = '''
            update Users set PNumber = %s
            Where Email = %s
            returning Email
        '''
        cursor.execute(query, (pNumber, email,))
        result = cursor.fetchone()[0]
        self.conn.commit()
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

    def confirmAccount(self, uid):
        cursor = self.conn.cursor()
        query = '''
            update Users set Confirmation = True
            Where UID = %s
        '''
        cursor.execute(query, (uid,))
        self.conn.commit()

    def getLoginAttempts(self, email):
        cursor = self.conn.cursor()
        query = '''
            Select logattempt
            From Users
            Where email = %s
        '''
        cursor.execute(query, (email,))
        attempts = cursor.fetchone()[0]
        return attempts

    def addToLoginAttempt(self, email, attempts):
        cursor = self.conn.cursor()
        query = '''
            update Users set logattempt = %s
            Where Email = %s
        '''
        cursor.execute(query, (attempts, email,))
        self.conn.commit()

    def resetLoginAttempt(self, email):
        cursor = self.conn.cursor()
        query = '''
            update Users set logattempt = %s
            Where Email = %s
        '''
        cursor.execute(query, (0, email,))
        self.conn.commit()

    def getBlockTime(self, email):
        cursor = self.conn.cursor()
        query = '''
            Select blocked
            From Users
            Where email = %s
        '''
        cursor.execute(query, (email,))
        bTime = cursor.fetchone()[0]
        return bTime


    def setBlockTime(self, email):
        try:
            cursor = self.conn.cursor()
            query = '''
              update Users set logattempt = %s
              Where Email = %s
          '''
            cursor.execute(query, (0, email,))

            bTime = datetime.datetime.now() + datetime.timedelta(hours= 1)
            query = '''
              update Users set blocked = %s
              Where Email = %s
          '''
            cursor.execute(query, (bTime, email,))
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            raise e

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = '''
            Select UID, FName, LName, Email, PNumber
            From Users
        '''
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getConfirmation(self, email):
        cursor = self.conn.cursor()
        query = '''
            Select Confirmation
            From Users
            Where Email = %s
        '''
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result is None:
            return result
        confirmation = result[0]
        return confirmation

    def getUserInfo(self, email, Role):
        cursor = self.conn.cursor()
        if Role == "C":
            query = '''
            Select FName, LName, Email, PNumber, CID
            From Users NATURAL INNER JOIN Client
            Where email = %s
        '''

        if Role == "A":
            query = '''
                        Select FName, LName, Email, PNumber, AID
                        From Users NATURAL INNER JOIN Admin
                        Where email = %s
                    '''

        if Role == "W":
            query = '''
                        Select FName, LName, Email, PNumber, WID
                        From Users NATURAL INNER JOIN Worker
                        Where email = %s
                    '''
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result