from celery import states
from celery.utils.log import get_task_logger

from app import celery_instance


logger = get_task_logger(__name__)


@celery_instance.task(bind=True)
def initial_hello(self):

    self.update_state(
        state=states.STARTED,
        meta={'done': 0, 'total': 100, 'message': "starting"})

    print("Initial hello asynchronously!")

    self.update_state(
        state=states.SUCCESS,
        meta={'done': 100, 'total': 100, 'message': 'done'})
