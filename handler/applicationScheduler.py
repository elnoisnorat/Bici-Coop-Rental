import traceback

import stripe

from app import scheduler, time, atexit
from dao.client import ClientDAO
from dao.rental import RentalDAO
import datetime


class SchedulerHandler:
    def wasDispatched(self, rid):
        """
        Method that verifies if the bicycle was dispatched after a certain time period
        :param rid: Rental ID
        :return: Nothing
        """
        print("ENTERED wasDispatched")
        rDao = RentalDAO()
        try:
            stripeID = rDao.getStripeToken(rid)
            rDao.wasDispatched(rid)
            if stripeID != 'CASH':
                stripe.Subscription.delete(stripeID)
            scheduler.remove_job('debt' + str(rid))
        except Exception as e:
            print("Something went wrong with schedule: rental" + str(rid))
            traceback.print_exc()

            scheduler.add_job(func=self.wasDispatched, args=[rid], trigger="date",
                              run_date=datetime.datetime.today() + datetime.timedelta(seconds=2),
                              id='rental' + str(rid))

    def hasDebt(self, rid):
        """
        Method that verifies if the bicycle was dispatched after a certain time period
        :param rid: Rental ID
        :return: Nothing
        """
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