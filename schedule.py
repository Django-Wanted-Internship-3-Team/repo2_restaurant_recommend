import subprocess

from apscheduler.schedulers.background import BackgroundScheduler


def run_data_file():
    subprocess.run(["python", "data.py"], check=True)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_data_file, "cron", hour=2, minute=30)
    scheduler.start()
