from .tasks import background_hello
from ..decorators import api_token_required


@api_token_required
def instant_hello():
    return 'Bienvenue, World!'


def celery_hello():
    background_hello.delay()
    return "Salut, c'est Celery!"
