"""
This file contains django settings to run tests with runtests.py
"""
SECRET_KEY = 'fake-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'test',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },
    'secondary': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test2',
        'USER': 'test',
        'PASSWORD': 'test',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },

    # I need separate connections for multiprocessing tests
    'test_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_test',
        'USER': 'test',
        'PASSWORD': 'test',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },
}

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django-clickhouse': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'infi.clickhouse-orm': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
}

INSTALLED_APPS = [
    "src",
    "tests"
]

CLICKHOUSE_DATABASES = {
    'default': {
        'db_name': 'test',
        'username': 'default',
        'password': ''
    },
    'secondary': {
        'db_name': 'test_2',
        'username': 'default',
        'password': ''
    },
    'no_migrate': {
        'db_name': 'test_3',
        'username': 'default',
        'password': '',
        'migrate': False
    },
    'readonly': {
        'db_name': 'test_3',
        'username': 'default',
        'password': '',
        'readonly': True
    }
}

CLICKHOUSE_SYNC_BATCH_SIZE = 5000

CLICKHOUSE_REDIS_CONFIG = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 8,
    'socket_timeout': 10
}

DATABASE_ROUTERS = ['tests.routers.SecondaryRouter']
