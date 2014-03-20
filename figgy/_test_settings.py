'''Settings for the tox testing'''
from figgy.settings import *

DEBUG = False

PASSWORD_HASHERS = (
    # Fast plz
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'figgy-test-unique-snowflake'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] [%(asctime)s] [%(name)s]: %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        'storage': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

NOSE_ARGS = [
    '--with-coverage',
    '--verbose',
    '--logging-clear-handlers',
    '--cover-package=storage,figgy',
    '-s',
]

TESTING = True

# Developers should always have a _local_tests.py file.
# Copy it from _local_tests.py.example and customize.
# If you need to locally override things (like NOSE_ARGS),
# add them to _local_tests.py
try:
    from figgy._local_tests import *
except ImportError as inst:
    print u"FYI: You have no figgy/_local_tests.py, but you should!"

