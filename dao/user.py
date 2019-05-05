import psycopg2
from config.dbconfig import pg_config
import datetime
from handler.newEmail import EmailHandler


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

            if Role == "Client":
                query = "insert into Client(UID, debtorflag) values (%s, FALSE)"

            if Role == "Admin":
                query = "insert into Admin(UID) values (%s)"

            if Role == "Worker":
                query = "insert into Worker(UID, Status) values (%s, 'ACTIVE')"

            cursor.execute(query, (uID,))
            eHand = EmailHandler()
            eHand.confirmationEmail(Email)
            self.conn.commit()
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

    def updateNames(self, email, fName, lName):
        cursor = self.conn.cursor()
        query = '''
            update Users set FName = %s, LName = 
            Where Email = %s
        '''
        cursor.execute(query, (fName, lName, email,))

    def updateName(self, email, fName):
        cursor = self.conn.cursor()
        query = '''
            update Users set FName = %s
            Where Email = %s
        '''
        cursor.execute(query, (fName, email,))

    def updateLName(self, email, uLName):
        cursor = self.conn.cursor()
        query = '''
            update Users set LName = %s
            Where Email = %s
        '''
        cursor.execute(query, (uLName, email,))

    def updatePassword(self, email, password):
        cursor = self.conn.cursor()
        query = '''
            update Users set password = crypt(%s,  gen_salt('bf'))
            Where Email = %s
        '''
        cursor.execute(query, (password, email,))
        self.conn.commit()

    def updatePNumber(self, email, pNumber):
        cursor = self.conn.cursor()
        query = '''
            update Users set PNumber = %s
            Where Email = %s
        '''
        cursor.execute(query, (pNumber, email,))
        self.conn.commit()

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
        if result is None:
            return result
        return result[0]

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

    def confirmAccount(self, email):
        cursor = self.conn.cursor()
        query = '''
            update Users set Confirmation = True
            Where email = %s and Confirmation = False
            Returning UID
        '''
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        self.conn.commit()
        if row is None:
            return row
        return row[0]


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
        return result[0]

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

    def checkCurrentPassword(self, email, oldPassword):
        cursor = self.conn.cursor()
        query = '''
                    Select *
                    From Users
                    Where email = %s and password = crypt(%s, password)
                '''
        cursor.execute(query, (email, oldPassword,))
        result = cursor.fetchone()
        if result is None:
            return False
        return True

    def getPhoneNumberByUID(self, reqID):
        cursor = self.conn.cursor()
        query = '''
                Select pnumber
                From Users
                Where UID = %s
                '''
        cursor.execute(query, (reqID,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def updateForgottenPassword(self, email, password):
        eHand = EmailHandler()
        try:
            cursor = self.conn.cursor()
            query = '''
                update Users set password = crypt(%s,  gen_salt('bf'))
                Where Email = %s
            '''
            cursor.execute(query, (password, email,))
            self.conn.commit()
            eHand.resetPassword(email, password)
        except Exception as e:
            self.conn.rollback()
            raise e




