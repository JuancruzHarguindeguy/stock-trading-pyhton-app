import schedule
import time
from scriptSnow import run_stock_job

from datetime import datetime

def basic_job():
    print("Job started at:", datetime.now())


# Run every minute
#schedule.every().minute.do(basic_job)
# Run every minute
schedule.every().day.at("07:00").do(run_stock_job)

while True:
    schedule.run_pending()
    time.sleep(1)