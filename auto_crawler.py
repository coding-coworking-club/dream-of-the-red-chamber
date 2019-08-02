# one method is time.sleep(86400)
# another is by datetime.datetime.now()

import os
import time
import datetime

now = datetime.datetime.now()

everyday_start_hour = 17
everyday_start_min  = 55

while True:
    now = datetime.datetime.now()
    
    if now.hour == everyday_start_hour and now.minute == everyday_start_min:
        os.system('python crawler.py')
        print(now)
    
    time.sleep(55)

