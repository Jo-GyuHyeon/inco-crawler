import time
import datetime
import schedule
import Manager

platform = "Naver"

Manager.initialize()

schedule.every().day.at("20:30").do(Manager.job)

while True:
    schedule.run_pending()
    time.sleep(60)
