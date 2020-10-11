import os
from celery import Celery
from celery.signals import worker_ready
from app import create_app


def create_celery(app):
    celery_instance = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery_instance.conf.update(app.config)

    class ContextTask(celery_instance.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_instance.Task = ContextTask
    return celery_instance


# this instance is to be used only to launch the worker process
celery_app = create_celery(create_app(os.environ.get('FLASK_CONFIG', 'default')))

# import the initial tasks for celery to discover them
from . import initial_task


# The celery worker in the Docker Compose file has been started with concurrency=2,
# using prefork execution pool. Here, one of those child processes in the prefork
# execution pool will be permanently occupied if a blocking task like AMQP Listener is started
# below. To increase number of child processes one of the following options should be chosen:
#
# #1 Increase concurrency,  but this is not advised as it is dependent on the number of CPUs in the machine
# OR
# #2 Change execution pool to Greenlets, then increase concurrency without worrying about the number of CPUs.
#
# Learn more:
# https://www.distributedpython.com/2018/10/26/celery-execution-pool/
@worker_ready.connect
def at_start(sender, **kwargs):
    with sender.app.connection() as conn:
        sender.app.send_task('app.worker.initial_task.initial_hello', connection=conn)
