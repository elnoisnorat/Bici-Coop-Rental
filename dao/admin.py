import psycopg2
from config.dbconfig import pg_config
class AdminDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def adminLogin(self, email, password):
        cur = self.conn.cursor()
        query ='''
            Select AID
            From Users natural inner join Admin
            Where email = %s and password = crypt(%s, password)
        '''
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

        aID = cur.fetchone()[0]
        return aID


