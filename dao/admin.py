import psycopg2
from config.dbconfig import pg_config
from config.encryption import SECRET_KEY

class AdminDAO:
    def __init__(self):
        self.conn = psycopg2._connect(pg_config['connection_url'])

    def adminLogin(self, email, password):
        cur = self.conn.cursor()
        # query ='''Select AID
        #     From Users natural inner join Admin
        #     Where PGP_SYM_DECRYPT(Users.Email::bytea, %s) = %s and password = crypt(%s, password);'''
        query ='''
            Select AID
            From Users natural inner join Admin
            Where email = %s and password = crypt(%s, password)
        '''
        #cur.execute(query, (SECRET_KEY, email, password))
        cur.execute(query, (email, password))

        row = cur.fetchone()
        if row is None:
            return row

        else:
            aID = row[0]

        return aID

    def insert(self, uid):
        return ''

    def getAdminByUID(self, uid):
        cur = self.conn.cursor()
        query ='''
            Select AID
            From Admin
            Where UID = %s
        '''
        cur.execute(query, (uid,))

        aID = cur.fetchone()
        if aID is None:
            return aID
        return aID[0]



