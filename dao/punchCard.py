import psycopg2
from config.dbconfig import pg_config


class PunchCardDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def inType(self, wid):
        cursor = self.conn.cursor()
        query = '''
             insert into PunchCard(wid, stampType, STAMP) VALUES (%s, %s, now())
        '''
        cursor.execute(query, (wid, 'In'))
        self.conn.commit()

    def outType(self, wid):
        cursor = self.conn.cursor()
        query = '''
             insert into PunchCard(wid, stampType, STAMP) VALUES (%s, %s, now())
        '''
        cursor.execute(query, (wid, 'Out'))
        self.conn.commit()