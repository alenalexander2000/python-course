"""Development settings."""

from .base import *


DEBUG = True

ALLOWED_HOSTS = [
    'ec2-18-205-246-156.compute-1.amazonaws.com',
    'uebt-demo.cied.in',
]

CORS_ORIGIN_WHITELIST = (
    'ec2-18-205-246-156.compute-1.amazonaws.com',
    'uebt-demo.cied.in',
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sparkpostmail.com'

# # Port for sending e-mail.
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'SMTP_Injection'
# EMAIL_HOST_PASSWORD = '3cf4f2e651ced1215c3daaa62fd69199da699238'

# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'auditordeskuebt',
        'USER': 'auditordeskuebt',
        'PASSWORD': 'auditordeskuebt',
        'PORT': '5432',
        'HOST': 'localhost'
    }
}

AWS_ACCESS_KEY_ID = 'AKIAI6DRR3OFXXM3YOAA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'auditordeskuebt-dev'
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = True

DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = 'media'
MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
# MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
# MEDIA_URL = '/media/'

# Redis setup for celery
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

ROOT_URL = 'ec2-18-205-246-156.compute-1.amazonaws.com'


if DEBUG is False:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }


# Spark post Email con figs

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'auditordeskuebt@gmail.com'
EMAIL_HOST_PASSWORD = 'admin@uebt'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
# SPARKPOST_OPTIONS = {
#     'track_opens': False,
#     'track_clicks': False,
#     'transactional': True,
# }
