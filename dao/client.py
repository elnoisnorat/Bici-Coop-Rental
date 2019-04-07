from config.dbconfig import pg_config
from flask import jsonify

import psycopg2

class ClientDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)
        self.conn.autocommit = False

    def clientLogin(self, email, password):
        cur = self.conn.cursor()
        query = '''
            Select CID
            From Users natural inner join Client
            Where email = %s and password = crypt(%s, password)
        '''
        cur.execute(query, (email, password))
        cID = cur.fetchone()[0]
        return cID

    def insert(self, form):
        try:
            cursor = self.conn.cursor()
            query = '''
                      insert into Users(FName, LName, password, PNumber, Email)
                      values (%s, %s, crypt(%s, %s), %s, %s) returning uID;
                    '''
            cursor.execute(query, (form['FName'], form['LName'], form['password'], 'password', form['PNumber'] , form['Email'],))
            uID = cursor.fetchone()[0]
            #self.conn.commit()
            #return uID
            query = "insert into Client(UID) values (%s) returning CID"
            cursor.execute(query, (uID,))
            cID = cursor.fetchone()
            self.conn.commit()
            pass
        except Exception as e:
            self.conn.rollback()
            raise e
        return cID

    def getClientByUID(self, uid):
        cursor = self.conn.cursor()
        query = '''
            Select *
            From Client
            Where UID = %s
        '''
        cursor.execute(query, (uid,))
        uID = cursor.fetchone()
        return uID

    def getUserByArguments(self):
        return ''

    def getUserWithSorting(self):
        return ''

    def getUserByArgumentsWithSorting(self):
        return ''

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




