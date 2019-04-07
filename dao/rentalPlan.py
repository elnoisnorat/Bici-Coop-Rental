import psycopg2
from config.dbconfig import pg_config
class RentalPlanDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2._connect(connection_url)

    def getRentalPlan(self):
        cursor = self.conn.cursor()
        query = "Select * From RentalPlan"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def editPlan(self):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query)
        self.conn.commit()
