import traceback

import psycopg2
from config.encryption import SECRET_KEY
from config.dbconfig import pg_config
import datetime
from handler.newEmail import EmailHandler


class UsersDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s sslmode=%s sslrootcert=%s" % (
            pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'],
            pg_config['mode'], pg_config['cert'])
        self.conn = psycopg2._connect(connection_url)
        # self.conn = psycopg2._connect(pg_config['connection_url'])

    def insert(self, FName, LName, password, PNumber, Email, Role):
        try:

            cursor = self.conn.cursor()
            query = ''' insert into Users(FName, LName, password, PNumber, Email,
                Confirmation, LogAttempt, Blocked)
                VALUES (  PGP_SYM_ENCRYPT(%s, %s),
                PGP_SYM_ENCRYPT(%s, %s),
                (crypt(%s, gen_salt('bf'))) ,
                PGP_SYM_ENCRYPT(%s, %s),
                PGP_SYM_ENCRYPT(%s, %s),
                %s,
                %s,
                %s
                returning UID;
                '''
            cursor.execute(query, (FName, SECRET_KEY, LName, SECRET_KEY, password, PNumber, SECRET_KEY, Email, SECRET_KEY, False, datetime.datetime.now(), 0,))
            # query = '''
            #       insert into Users(FName, LName, password, PNumber, Email, confirmation, blocked, logattempt)
            #       values (%s, %s, crypt(%s, gen_salt('bf')), %s, %s, %s, %s, %s) returning uID;
            #       '''
            # cursor.execute(query,
            #            (FName, LName, password, PNumber, Email, False, datetime.datetime.now(), 0))
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
        query = '''select UID,
            PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
            PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
            PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
            PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber
            from Users where UID = %s;
    
            '''

        # query = '''
        #     Select UID, FName, LName, Email, PNumber
        #     From Users
        #     Where UID = %s
        # '''
        cursor.execute(query, (SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY, uid,))
        # cursor.execute(query, (uid,))
        result = cursor.fetchone()
        return result

    def getUserByEmail(self, email):
        cursor = self.conn.cursor()
        query = '''select UID,
            PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
            PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
            PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
            PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber
            from Users where  PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s;

            '''
        # query = '''
        #     Select UID, FName, LName, Email, PNumber
        #     From Users
        #     Where Email = %s
        # '''
        cursor.execute(query, (SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY, email, ))
        # cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result

    def updateNames(self, email, fName, lName):
        cursor = self.conn.cursor()
        query = '''update Users set FName = PGP_SYM_ENCRYPT(%s, %s),
            LName =PGP_SYM_ENCRYPT(%s, %s)
            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s
            '''
        # query = '''
        #     update Users set FName = %s, LName = %s
        #     Where Email = %s
        # '''
        cursor.execute(query, (fName, SECRET_KEY, lName, SECRET_KEY, SECRET_KEY, email, ))
        self.conn.commit()
        # cursor.execute(query, (fName, lName, email,))

    def updateName(self, email, fName):
        cursor = self.conn.cursor()
        query = '''update Users set FName = PGP_SYM_ENCRYPT(%s, %s)

                    Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s
                    '''
        # query = '''
        #     update Users set FName = %s
        #     Where Email = %s
        # '''
        cursor.execute(query, (fName, SECRET_KEY, SECRET_KEY, email, ))
        self.conn.commit()

        # cursor.execute(query, (fName, email,))

    def updateLName(self, email, uLName):
        cursor = self.conn.cursor()
        query = '''update Users set LName = PGP_SYM_ENCRYPT(%s, %s)

                            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s
                            '''
        # query = '''
        #     update Users set LName = %s
        #     Where Email = %s
        # '''
        cursor.execute(query, (uLName, SECRET_KEY, SECRET_KEY, email, ))
        self.conn.commit()

        # cursor.execute(query, (uLName, email,))

    def updatePassword(self, email, password):
        cursor = self.conn.cursor()
        query = '''update Users set password = crypt(%s,  gen_salt('bf'))
            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s'''
        # query = '''
        #     update Users set password = crypt(%s,  gen_salt('bf'))
        #     Where Email = %s
        # '''
        cursor.execute(query, (password, SECRET_KEY, email,))
        # cursor.execute(query, (password, email,))
        self.conn.commit()

    def updatePNumber(self, email, pNumber):
        cursor = self.conn.cursor()
        query ='''update Users set pnumber = PGP_SYM_ENCRYPT(%s, %s)

                                    Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s
                                    '''
        # query = '''
        #     update Users set PNumber = %s
        #     Where Email = %s
        # '''
        cursor.execute(query, (pNumber, SECRET_KEY, SECRET_KEY, email, ))
        # cursor.execute(query, (pNumber, email,))
        self.conn.commit()

    def getUserWithCID(self, cid):
        cursor = self.conn.cursor()
        query ='''select UID,
                    PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
                    PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
                    PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
                    PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber
                    from Users natural inner join Client where  CID = %s;

                    '''
        # query = '''
        #     Select UID, FName, LName, Email, PNumber
        #     From Users natural inner join Client
        #     Where CID = %s
        # '''
        cursor.execute(query, (SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY, cid,))
        # cursor.execute(query, (cid,))
        result = cursor.fetchone()
        return result

    def getUserIDByEmail(self, Email):
        cursor = self.conn.cursor()
        query ='''  Select UID
            From Users
            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s'''
        # query = '''
        #     Select UID
        #     From Users
        #     Where Email = %s
        # '''
        cursor.execute(query, (SECRET_KEY, Email,))
        # cursor.execute(query, (Email,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def getUserWithWID(self, wid):
        cursor = self.conn.cursor()
        query ='''select UID,
                           PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
                           PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
                           PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
                           PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber
                           from Users natural inner join Worker where  wid = %s;

                           '''
        # query = '''
        #     Select UID, FName, LName, Email, PNumber
        #     From Users natural inner join Worker
        #     Where WID = %s
        # '''
        cursor.execute(query, (SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY, wid,))
        # cursor.execute(query, (wid,))
        result = cursor.fetchone()
        return result

    def confirmAccount(self, email):
        cursor = self.conn.cursor()
        query ='''  update Users set Confirmation = True
            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s
             and Confirmation = False
            Returning UID  '''
        # query = '''
        #     update Users set Confirmation = True
        #     Where email = %s and Confirmation = False
        #     Returning UID
        # '''
        cursor.execute(query, (SECRET_KEY, email,))
        # cursor.execute(query, (email,))
        row = cursor.fetchone()
        self.conn.commit()
        if row is None:
            return row
        return row[0]


    def getLoginAttempts(self, email):
        cursor = self.conn.cursor()
        query ='''Select logattempt
            From Users
            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s'''
        # query = '''
        #     Select logattempt
        #     From Users
        #     Where email = %s
        # '''
        cursor.execute(query, (SECRET_KEY, email,))
        # cursor.execute(query, (email,))
        attempts = cursor.fetchone()[0]
        return attempts

    def addToLoginAttempt(self, email, attempts):
        cursor = self.conn.cursor()
        query ='''update Users set logattempt = %s
            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s'''
        # query = '''
        #     update Users set logattempt = %s
        #     Where Email = %s
        # '''
        cursor.execute(query, (attempts, SECRET_KEY, email,))
        # cursor.execute(query, (attempts, email,))
        self.conn.commit()

    def resetLoginAttempt(self, email):
        cursor = self.conn.cursor()
        query ='''update Users set logattempt = %s
            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s'''
        # query = '''
        #     update Users set logattempt = %s
        #     Where Email = %s
        # '''
        cursor.execute(query, (0, SECRET_KEY, email,))
        # cursor.execute(query, (0, email,))
        self.conn.commit()

    def getBlockTime(self, email):
        cursor = self.conn.cursor()
        query =''' Select blocked
            From Users
            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s'''
        # query = '''
        #     Select blocked
        #     From Users
        #     Where email = %s
        # '''
        cursor.execute(query, (SECRET_KEY, email,))
        # cursor.execute(query, (email,))
        bTime = cursor.fetchone()[0]
        return bTime


    def setBlockTime(self, email):
        try:
            cursor = self.conn.cursor()
            query =''' update Users set logattempt = %s
              Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s'''
          #   query = '''
          #     update Users set logattempt = %s
          #     Where Email = %s
          # '''
            cursor.execute(query, (0, SECRET_KEY, email,))
            # cursor.execute(query, (0, email,))

            bTime = datetime.datetime.now() + datetime.timedelta(hours= 1)
            query ='''update Users set blocked = %s
              Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s'''
          #   query = '''
          #     update Users set blocked = %s
          #     Where Email = %s
          # '''
            cursor.execute(query, (bTime, SECRET_KEY, email,))
            # cursor.execute(query, (bTime, email,))
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            raise e

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query ='''select UID,
                            PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
                            PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
                            PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
                            PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber
                            from Users;

                            '''
        # query = '''
        #     Select UID, FName, LName, Email, PNumber
        #     From Users
        # '''
        cursor.execute(query, (SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY, ))
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getConfirmation(self, email):
        cursor = self.conn.cursor()
        query ='''  Select Confirmation
            From Users
            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s'''
        # query = '''
        #     Select Confirmation
        #     From Users
        #     Where Email = %s
        # '''
        cursor.execute(query, (SECRET_KEY, email,))
        # cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def getUserInfo(self, email, Role):
        cursor = self.conn.cursor()
        if Role == "C":
            query ='''select
                                        PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
                                        PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
                                        PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
                                        PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber,
                                        CID
                                        from Users NATURAL INNER JOIN Client Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s;

                                        '''
        #     query = '''
        #     Select FName, LName, Email, PNumber, CID
        #     From Users NATURAL INNER JOIN Client
        #     Where email = %s
        # '''

        if Role == "A":
            query ='''select
                                                    PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
                                                    PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
                                                    PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
                                                    PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber,
                                                    AID
                                                    from Users NATURAL INNER JOIN Admin Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s;

                                                    '''
            # query = '''
            #             Select FName, LName, Email, PNumber, AID
            #             From Users NATURAL INNER JOIN Admin
            #             Where email = %s
            #         '''

        if Role == "W":
            query ='''select
                                                               PGP_SYM_DECRYPT(Users.FName::bytea, %s) as Fname,
                                                               PGP_SYM_DECRYPT(Users.Lname::bytea, %s) as Lname,
                                                               PGP_SYM_DECRYPT(Users.Email::bytea, %s) as Email,
                                                               PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber,
                                                               WID
                                                               from Users NATURAL INNER JOIN Worker Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s;

                                                               '''
            # query = '''
            #             Select FName, LName, Email, PNumber, WID
            #             From Users NATURAL INNER JOIN Worker
            #             Where email = %s
            #         '''
        cursor.execute(query, (SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY, SECRET_KEY, email, ))
        # cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result

    def checkCurrentPassword(self, email, oldPassword):
        cursor = self.conn.cursor()
        query ='''
                            Select uid
                            From Users
                            Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s and password = crypt(%s, password)
                        '''
        # query = '''
        #             Select *
        #             From Users
        #             Where email = %s and password = crypt(%s, password)
        #         '''
        cursor.execute(query, (SECRET_KEY, email, oldPassword,))
        # cursor.execute(query, (email, oldPassword,))
        result = cursor.fetchone()
        if result is None:
            return False
        return True

    def getPhoneNumberByUID(self, reqID):
        cursor = self.conn.cursor()
        query ='''Select PGP_SYM_DECRYPT(Users.PNumber::bytea, %s) as PNumber,
                From Users
                Where UID = %s'''
        # query = '''
        #         Select pnumber
        #         From Users
        #         Where UID = %s
        #         '''
        cursor.execute(query, (SECRET_KEY, reqID,))
        # cursor.execute(query, (reqID,))
        result = cursor.fetchone()
        if result is None:
            return result
        return result[0]

    def updateForgottenPassword(self, email, password):
        eHand = EmailHandler()
        try:
            query ='''update Users set password = crypt(%s,  gen_salt('bf')) Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s'''
            cursor = self.conn.cursor()
            # query = '''
            #     update Users set password = crypt(%s,  gen_salt('bf'))
            #     Where Email = %s
            # '''
            cursor.execute(query, (password, SECRET_KEY, email,))
            # cursor.execute(query, (password, email,))
            self.conn.commit()
            eHand.resetPassword(email, password)
        except Exception as e:
            traceback.print_exc()
            self.conn.rollback()
            raise e




