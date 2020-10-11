from .tasks import background_hello


def instant_hello():
    return 'Bienvenue, World!'


def celery_hello():
    background_hello.delay()
    return "Salut, c'est Celery!"
