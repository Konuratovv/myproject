from celery import shared_task
import time


@shared_task
def simple_task():
    time.sleep(5)
    print('taks completed!!!')
