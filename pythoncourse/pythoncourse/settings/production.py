"""Production settings."""

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Not showing the errors

ALLOWED_HOSTS = [
    'ec2-18-184-4-160.eu-central-1.compute.amazonaws.com',
    'uebt.auditordesk.com',
]

CORS_ORIGIN_WHITELIST = (
    'ec2-18-184-4-160.eu-central-1.compute.amazonaws.com',
    'uebt.auditordesk.com',
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sparkpostmail.com'

# Port for sending e-mail.
EMAIL_PORT = 587
EMAIL_HOST_USER = 'SMTP_Injection'
EMAIL_HOST_PASSWORD = '3cf4f2e651ced1215c3daaa62fd69199da699238'

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'auditordeskuebt',
        'USER': 'auditordeskuebt',
        'PASSWORD': 'auditordeskuebt',
        'PORT': '5432'
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
# MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
# MEDIA_URL = '/media/'

ROOT_URL = ''

# if not DEBUG:
#     LOGGING = {
#         'version': 1,
#         'disable_existing_loggers': False,
#         'handlers': {
#             'slack-error': {
#                 'level': 'ERROR',
#                 'class': 'auditordeskpragati.slack_loghandler.SlackLogHandler',
#                 'logging_url': 'https://hooks.slack.com/services/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',
#                 'stack_trace': True
#             },
#         },
#         'loggers': {
#             'django.request': {
#                 'handlers': ['slack-error'],
#                 'level': 'ERROR',
#                 'propagate': True,
#             }
#         },
#     }
