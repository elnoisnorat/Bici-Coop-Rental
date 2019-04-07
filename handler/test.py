from datetime import datetime

import schedule
import time
import datetime

def job():
    print("I'm working...")

schedule.every()
End = False
Finish = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
while not End:
    schedule.run_pending()
    Current = datetime.datetime.utcnow()
    if Finish < Current:
        End = True

