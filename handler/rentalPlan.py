from flask import jsonify

from dao.rentalPlan import RentalPlanDAO


class RentalPlanHandler:
    def build_plan_dict(self, row):
        '''
        Plan attribute
        '''

    def getRentalPlan(self):
        rDao = RentalPlanDAO()
        plan_list = rDao.getRentalPlan()
        result_list = []
        for row in plan_list:
            result = self.build_plan_dict(row)
            result_list.append(result)
        return jsonify(RentalPlan=result_list)

    def editPlan(self, json):
        '''
            Wait for table:
        '''
        rDao = RentalPlanDAO().editPlan()
        return jsonify('Rental Plan update was successful.')
