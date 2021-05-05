from celery import states
from celery.utils.log import get_task_logger
import time

from app import celery_instance


logger = get_task_logger(__name__)


@celery_instance.task(bind=True)
def background_hello(self):

    self.update_state(
        state=states.STARTED,
        meta={'done': 0, 'total': 100, 'message': "starting"})

    print("Hello asynchronously started!")
    time.sleep(5)

    self.update_state(
        state=states.STARTED,
        meta={'done': 50, 'total': 100, 'message': "starting"})

    time.sleep(5)
    print("Hello asynchronously over!")

    self.update_state(
        state=states.SUCCESS,
        meta={'done': 100, 'total': 100, 'message': 'done'})
