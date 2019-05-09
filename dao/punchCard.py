import psycopg2
from config.dbconfig import pg_config


class PunchCardDAO:

    def __init__(self):
        self.conn = psycopg2._connect(pg_config['connection_url'])

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