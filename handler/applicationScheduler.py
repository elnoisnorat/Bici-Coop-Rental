import traceback

from app import scheduler, time, atexit
from dao.client import ClientDAO
from dao.rental import RentalDAO
import datetime


class SchedulerHandler:
    def wasDispatched(self, rid):
        print("ENTERED wasDispatched")
        rDao = RentalDAO()
        try:
            rDao.wasDispatched(rid)
            scheduler.remove_job('debt' + str(rid))
            #scheduler.remove_job('rental' + str(rid))
        except Exception as e:
            print("Something went wrong with schedule: rental" + str(rid))
            traceback.print_exc()

            scheduler.add_job(func=self.wasDispatched, args=[rid], trigger="date",
                              run_date=datetime.datetime.today() + datetime.timedelta(seconds=2),
                              id='rental' + str(rid))

    def hasDebt(self, rid):
        print("ENTERED hasDebt")
        try:
            rDao = RentalDAO()
            cid = rDao.getClientByRID(rid)
            cDao = ClientDAO()
            cDao.setDebtorFlag(cid)
#            scheduler.remove_job('debt' + str(rid))
        except Exception as e:
            traceback.print_exc()
            pass


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