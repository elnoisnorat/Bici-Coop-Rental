import psycopg2
from config.dbconfig import pg_config
class RentalPlanDAO:
    def __init__(self):
        self.conn = psycopg2._connect(pg_config['connection_url'])

    def getRentalPlan(self):
        cursor = self.conn.cursor()
        query = "Select * From Plans"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPlan(self, reqPlan):
        cur = self.conn.cursor()
        query = " Select name, amount from plans WHERE PID = %s"
        cur.execute(query, (reqPlan))
        result = cur.fetchone()
        return result

    def getOverduePlan(self):
        cur = self.conn.cursor()
        query = " Select name, amount from plans WHERE PID = 2"
        cur.execute(query)
        print("Query:\n")
        result = cur.fetchone()
        print(result[0][0])
        return result


    def editPlan(self, name, amount):
        cur = self.conn.cursor()
        query = " UPDATE Plans set name = %s, amount = %s WHERE PID = 1"
        cur.execute(query, (name, amount))
        self.conn.commit()
