import psycopg2
from config.dbconfig import pg_config

class PriceDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s sslmode=%s sslrootcert=%s" % (
            pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'],
            pg_config['mode'], pg_config['cert'])
        self.conn = psycopg2._connect(connection_url)
        # self.conn = psycopg2._connect(pg_config['connection_url'])
    def getPrice(self):
        cursor = self.conn.cursor()
        query = '''
             Select *
             From Price
         '''
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result