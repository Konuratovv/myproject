from celery import shared_task
import time


@shared_task()
def simple_task():
    print('taks completed!!!')
