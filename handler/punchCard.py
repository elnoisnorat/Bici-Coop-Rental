from dao.punchCard import PunchCardDAO

class PunchCardHandler:
    def inType(self, wid):
        pDao = PunchCardDAO()
        pDao.inType(wid)

    def outType(self, wid):
        pDao = PunchCardDAO()
        print(wid)
        pDao.outType(wid)
