"""Local Settings for cbsoft are specified here."""

from .base import *
# import djcelery

# djcelery.setup_loader()
# BROKER_URL = 'django://'

ROOT_URL = 'http://localhost:8000'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pythoncourse',
        'USER': 'sooraj-dev',
        'PASSWORD': 'deadpool',
        'PORT': '5432',
        'HOST': 'localhost'
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Redis setup for celery.
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Spark post Email con figs

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sparkpostmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'SMTP_Injection'
# EMAIL_HOST_PASSWORD = '3cf4f2e651ced1215c3daaa62fd69199da699238'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# SPARKPOST_OPTIONS = {
#     'track_opens': False,
#     'track_clicks': False,
#     'transactional': True,
# }
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'soorajparakkattil@gmail.com'
EMAIL_HOST_PASSWORD = 'Parakkatt11@1'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
