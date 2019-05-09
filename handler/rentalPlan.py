import stripe
from flask import jsonify

from dao.rentalPlan import RentalPlanDAO


class RentalPlanHandler:
    def build_plan_dict(self, row):
        result = {}
        result['ID'] = row[0]
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

    def getPlan(self, reqPlan):
        rDao = RentalPlanDAO()
        try:
            result = rDao.getPlan()
            return result
            pass
        except Exception as e:
           raise e

    def getOverduePlan(self):
        rDao = RentalPlanDAO()
        try:
            result = rDao.getOverduePlan()
            return result
            pass
        except Exception as e:
            raise e

    def editPlan(self, form):
        rDao = RentalPlanDAO()
        try:
            name = form['name']
            amount = form['amount']

            response = jsonify(stripe.Plan.create(
                id=name,
                amount=amount,
                interval="week",
                product={
                    "name": "Rental"
                },
                currency="usd",
            ))
            rDao.editPlan(name, amount)
        except Exception as e:
            return jsonify(Error="An error has occurred. Please verify the submitted arguments."), 400

        return jsonify('Rental Plan update was successful.')
