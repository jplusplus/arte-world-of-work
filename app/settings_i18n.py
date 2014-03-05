from settings import *

without_app = lambda el: el.startswith('app.')

INSTALLED_APPS = filter(
    without_app,
    INSTALLED_APPS) + (
        'translations',
        'core'
    )