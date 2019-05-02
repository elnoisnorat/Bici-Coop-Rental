from config.dbconfig import pg_config
import psycopg2

class FinancialDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def getFinancialReport(self):
        cursor = self.conn.cursor()
        query = '''
            Select count(*)
            From Rental
            Where current_date - STime :: date < 7
        '''
        cursor.execute(query)
        rentals = cursor.fetchone()[0]

        query = '''
            Select sum(cost)
            From Transactions
            Where status != 'FAILED' and current_date - stamp :: date < 7
        '''
        cursor.execute(query)
        costs = cursor.fetchone()[0]
        result = {
            "Number of Rentals": rentals,
            "Money earned": costs
        }
        return result