from datetime import datetime
from app import scheduler, time, atexit
import schedule
import time
#import datetime
from dao.client import ClientDAO
from dao.rental import RentalDAO


class SchedulerHandler:
    def wasDispatched(self, rid):
        print("ENTERED wasDispatched")
        rDao = RentalDAO()
        rDao.wasDispatched(rid[0])
        scheduler.remove_job('rental' + str(rid[0]))

    def hasDebt(self, rid):
        print("ENTERED hasDebt")
        rDao = RentalDAO()
        cid = rDao.getClientByRID(rid[0])
        cDao = ClientDAO()
        cDao.setDebtorFlag(cid)
        scheduler.remove_job('debt' + str(rid[0]))


# schedule.every()
# End = False
# Finish = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
# while not End:
#     schedule.run_pending()
#     Current = datetime.datetime.utcnow()
#     if Finish < Current:
#         End = True
# def job(number):
#     print("I'm working on #:" + number)
#
# scheduler.add_job(func=job(4), trigger="interval", seconds=3)
# scheduler.start()

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())