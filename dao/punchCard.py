class PunchCardDAO:
    def inType(self, wid):
        cursor = self.conn.cursor()
        query = '''
             insert into PunchCard(wid, stampType, STAMP) VALUES (%s, %s, now();)
        '''
        cursor.execute(query, (wid, 'In'))
        self.conn.commit()

    def outType(self, wid):
        cursor = self.conn.cursor()
        query = '''
             insert into PunchCard(wid, stampType, STAMP) VALUES (%s, %s, now();)
        '''
        cursor.execute(query, (wid, 'Out'))
        self.conn.commit()