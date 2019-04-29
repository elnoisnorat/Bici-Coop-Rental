from flask import jsonify

from dao.rentalPlan import RentalPlanDAO


class RentalPlanHandler:
    def build_plan_dict(self, row):
        result = {}
        result['Plan Name'] = row[1]
        result['Cost'] = row[2]
        return result

    def getRentalPlan(self):
        rDao = RentalPlanDAO()
        plan_list = rDao.getRentalPlan()
        result_list = []
        for row in plan_list:
            result = self.build_plan_dict(row)
            result_list.append(result)
        return jsonify(RentalPlan=result_list)

    def editPlan(self, json):
        try:
            # Json entries
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        rDao = RentalPlanDAO().editPlan()
        return jsonify('Rental Plan update was successful.')
