from flask import jsonify

from dao.financial import FinancialDAO


class FinancialHandler:

    def getFinancialReport(self, form):
        fDao = FinancialDAO()
        report = fDao.getFinancialReport()
        return jsonify(report)
