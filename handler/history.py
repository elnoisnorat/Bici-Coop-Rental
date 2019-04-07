from dao.history import HistoryDAO
from flask import jsonify


class HistoryHandler:
    def build_rentalR_dict(self,row):
        result = {}
        result['Worker Name'] = row[0]
        result['Worker Last Name'] = row[1]
        result['Rental ID'] = row[2]
        result['Bicycle ID'] = row[3]
        result['License Plate'] = row[4]
        return result

    def build_rentalD_dict(self, row):
        result = {}
        result['Worker Name'] = row[0]
        result['Worker Last Name'] = row[1]
        result['Rental ID'] = row[2]
        result['Bicycle ID'] = row[3]
        result['License Plate'] = row[4]
        return result

    def build_maintenanceR_dict(self, row):
        result = {}
        result['Worker Name'] = row[0]
        result['Worker Last Name'] = row[1]
        result['Maintenance ID'] = row[2]
        result['Bicycle ID'] = row[3]
        result['License Plate'] = row[4]
        return result

    def build_maintenanceS_dict(self, row):
        result = {}
        result['Worker Name'] = row[0]
        result['Worker Last Name'] = row[1]
        result['Maintenance ID'] = row[2]
        result['Bicycle ID'] = row[3]
        result['License Plate'] = row[4]
        return result

    def build_serviceMaintenanceS_dict(self, row):
        result = {}
        result['Worker Name'] = row[0]
        result['Worker Last Name'] = row[1]
        result['Personal Maintenance ID'] = row[2]
        result['Bicycle'] = row[3]
        return result

    def build_decomissionR_dict(self, row):
        result = {}
        result['Worker Name'] = row[0]
        result['Worker Last Name'] = row[1]
        result['Decomission Request ID'] = row[2]
        result['Bicycle ID'] = row[3]
        return result

    def getRentalReceiverHistory(self, form):
    def getRentalDispatcherHistory(self, form):
    def getMaintenanceRequesterHistory(self, form):
    def getMaintenanceServerHistory(self, form):
    def getServiceMaintenanceServerHistory(self, form):
    def getDecomissionRequestHistory(self, form):

    def getAllWorkerHistory(self, form):
        hDao = HistoryDAO()
        FName = form['FName']
        LName = form['LName']
        wid = form['wid']
        args = []
        kargs = []
        for arg in form:
            if form[arg]:
                args.append(arg)
                kargs.append(form[arg])

        if wid or (FName and LName):
            receiverH = hDao.getRentalReceiverHistory(args, kargs)
            dispatcherH = hDao.getRentalDispatcherHistory(args, kargs)
            requesterH = hDao.getMaintenanceRequesterHistory(args, kargs)
            serverrH = hDao.getMaintenanceServerHistory(args, kargs)
            serverMH = hDao.getServiceMaintenanceServerHistory(args, kargs)
            decomRequestH = hDao.getDecomissionRequestHistory(args, kargs)
            receiver_list = []
            dispatcher_list = []
            requester_list = []
            server_list = []
            serverS_list = []

            for row in receiverH:
                result = self.build_rentalR_dict(row)
                receiver_list.append(result)
            for row in dispatcherH:
                result = self.build_rentalD_dict(row)
                dispatcher_list.append(result)
            for row in requesterH:
                result = self.build_maintenanceR_dict(row)
                requester_list.append(result)
            for row in serverrH:
                result = self.build_maintenanceS_dict(row)
                server_list.append(result)
            for row in serverMH:
                result = self.build_serviceMaintenanceS_dict(row)
                serverS_list.append(result)
            for row in decomRequestH:
                result = self.build_decomissionR_dict(row)
                serverS_list.append(result)
            return jsonify({
                'ReceiveHistory':receiver_list,
                'DispatcherHistory': dispatcher_list,
                'RequesterHistory' : requester_list,
                'ServerHistory'  : server_list,
                'PersonalServerHistory' : serverS_list
            })
        else:
            return jsonify(Error="No worker given.")

