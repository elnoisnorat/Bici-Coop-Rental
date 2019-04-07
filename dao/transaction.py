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

    def newTransactionWithCash(self, cid, pMethod): #NEEDS QUERY
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
