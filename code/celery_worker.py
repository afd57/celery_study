import random
from time import sleep
from celery import Celery, shared_task
from celery.utils.log import get_task_logger
from click import Option

# Initialize celery
celery = Celery('tasks', broker='redis://localhost:6379/0', backend='db+sqlite:///celery.sqlite')

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)
# Create Order - Run Asynchronously with celery
# Example process of long running task

class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@celery.task(bind=True,
             autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 7, 'countdown': 5},
             retry_backoff=True,
             track_started=True)
def create_long_task(self, name, quantity):
    
    # 5 seconds per 1 order
    complete_time_per_item = 5
    sleep(complete_time_per_item * quantity)
    celery_log.info(f"Order Complete!")
    return {"message": f"Hi {name}, Your order has completed!",
            "order_quantity": quantity}