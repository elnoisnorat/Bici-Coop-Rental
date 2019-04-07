class HistoryDAO:
    def getRentalReceiverHistory(self, args, kargs):
        cursor = self.conn.cursor()

        if len(args)==0:
            query = '''

          '''

        else:
            query = '''

            '''

        cursor.execute(query, (cID,))

        result = []
        for row in cursor:
            result.append(row)

        return result

    def getRentalDispatcherHistory(self, args):
        pass

    def getMaintenanceRequesterHistory(self, args):
        pass

    def getMaintenanceServerHistory(self, args):
        pass

    def getServiceMaintenanceServerHistory(self, args):
        pass

    def getDecomissionRequestHistory(self, args):
        pass