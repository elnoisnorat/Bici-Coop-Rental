import psycopg2
from config.dbconfig import pg_config

class PriceDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

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