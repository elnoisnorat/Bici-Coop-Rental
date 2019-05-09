import psycopg2
from config.dbconfig import pg_config

class PriceDAO:

    def __init__(self):
        self.conn = psycopg2._connect(pg_config['connection_url'])

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