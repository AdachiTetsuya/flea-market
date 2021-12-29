from .settings_common import *

DEBUG = True

ALLOWED_HOST = []

MEDIA_ROOT = os.path.join(BASE_DIR,'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'