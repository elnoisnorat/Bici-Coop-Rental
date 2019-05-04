import datetime

from config.dbconfig import pg_config
import psycopg2

class TransactionDAO:

    def __init__(self):
         connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
         self.conn = psycopg2._connect(connection_url)

    def getAllTransactions(self):
        cursor = self.conn.cursor()
        query = "SELECT TID, Stamp, token, FName, LName, LP FROM Transactions natural inner join Client natural inner join Users natural inner join Bike;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
            query = "SELECT FName, LName FROM Transactions natural inner join Worker natural inner join User;"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByClientId(self, cID):
        cursor = self.conn.cursor()
        query = "SELECT TID, Stamp, token, FName, LName, LP FROM Transactions natural inner join Client natural inner join User natural inner join Bike Where CID = %s;"
        cursor.execute(query, (cID,))
        result = []
        for row in cursor:
            result.append(row)
        query = "SELECT FName, LName FROM Transactions natural inner join Worker natural inner join User Where CID = %s;"
        cursor.execute(query, (cID,))
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByBicycleId(self,bID):
        cursor = self.conn.cursor()
        query = "SELECT TID, Stamp, token, FName, LName, LP FROM Transactions natural inner join Client natural inner join User natural inner join Bike Where BID = %s;"
        cursor.execute(query, (bID,))
        result = []
        for row in cursor:
            result.append(row)
        query = "SELECT FName, LName FROM Transactions natural inner join Worker natural inner join User Where BID = %s;"
        cursor.execute(query, (bID,))
        for row in cursor:
            result.append(row)
        return result

    def newTransaction(self, token, cid, amount, cost, duedate):
        try:
            cursor = self.conn.cursor()
            query = '''
              UPDATE bike SET bikestatus = 'RESERVED' 
              WHERE BID in (SELECT bid from bike 
                            where bikestatus = 'AVAILABLE' limit %s) 
                            returning bid
                    '''
            cursor.execute(query, (amount,))

            print("RESERVATION")

            query = '''
                INSERT INTO transactions(stamp, token, cid, status, cost) 
                VALUES (now(), %s, %s, 'COMPLETED', %s) 
                returning TID
            '''
            cursor.execute(query, (token, cid, cost))
            tID = cursor.fetchone()[0]

            print("TRANSACTION")
            print(amount)
            for iteration in range(amount):
                query = '''
                  INSERT INTO Rental(stime, client, dueDate) 
                  VALUES (now(), %s , %s) 
                  RETURNING RID;
                '''
                cursor.execute(query, (cid, duedate))
                rID = cursor.fetchone()[0]
                print(rID)
                query = '''
                  INSERT INTO RentLink(RID, TID) 
                  VALUES (%s, %s);
                        '''
                cursor.execute(query, (rID, tID,))
                print(iteration)
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            print(e)
            raise e
        return tID

    def newTransactionWithCreditCard(self, cid, pMethod): #NEEDS QUERY
        #cursor = self.conn.cursor()
        #query = '''
        #  insert into Transaction()
        #  values () returning TID;
        #'''
        #cursor.execute(query, ))
        #tID = cursor.fetchone()[0]
        #self.conn.commit()
        #return tID
        return 1
