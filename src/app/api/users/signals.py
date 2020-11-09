from blinker import Namespace
from flask import current_app


oneflask_users_signals = Namespace()
admin_user_post_save = oneflask_users_signals.signal('admin-user-post-save')
client_user_post_save = oneflask_users_signals.signal('client-user-post-save')


@admin_user_post_save.connect
def admin_user_post_save_action(instance, **kw):
    current_app.logger.info("admin_user_post_save_action fired")
    if 'created' in kw and kw['created']:
        pass


@client_user_post_save.connect
def client_user_post_save_action(instance, **kw):
    current_app.logger.info("client_user_post_save fired")
    if 'created' in kw and kw['created']:
        pass


