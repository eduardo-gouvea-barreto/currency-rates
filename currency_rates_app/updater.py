from apscheduler.schedulers.background import BackgroundScheduler

from currency_rates_app.services.fetch_data_service import insert_today_rates


def start():
    """
    Calls 4 times a day for function to insert today's currency rates for all currencies in database.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(insert_today_rates, 'interval', minutes=360)
    scheduler.start()
