from time import sleep
from celery import shared_task
from .functions import countC, spin_manager, market_create


@shared_task
def create_spinwheel():
    """ wheel instance to be executed every 5 minutes"""
    spin_manager()


@shared_task
def start_count_down():
    """ precise spin timer task"""

    sleep(16)  # spin time then
    countC(280)  # kick up the timer   # 277 + 16 = 296 seconds = 4.8 minutes


@shared_task
def create_market():
    """ wheel instance to be executed every 5 minutes"""
    market_create()
