from blinker import Namespace
from flask import current_app


oneflask_users_signals = Namespace()
user_post_save = oneflask_users_signals.signal('user-post-save')


@user_post_save.connect
def user_post_save_action(instance, **kw):
    current_app.logger.info("user_post_save_action fired")
    if 'created' in kw and kw['created']:
        pass
