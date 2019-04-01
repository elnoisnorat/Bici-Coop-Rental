from flask import jsonify

from dao.price import PriceDAO


class PriceHandler:
    def build_price_dict(self, row):
        result = {}
        result['Rental Period'] = row[0]
        result['Price($)'] = row[1]
        return result

    def getPrice(self):
        pDao = PriceDAO()
        price_list = pDao.getPrice()

        result_list = []
        for row in price_list:
            result = self.build_price_dict(row)
            result_list.append(result)

        return jsonify(PriceList= result_list)


