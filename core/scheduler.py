import schedule
import time

def job():
    print("Run fetchers and telegram delivery here")

def run_scheduler():
    schedule.every().day.at("06:00").do(job)
    schedule.every().day.at("18:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(30)
