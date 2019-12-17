from carsharing.settings import *
from envparse import env

env.read_envfile()

DEBUG = False

ALLOWED_HOSTS = ['carsharing.ru', '0.0.0.0', 'localhost', '170.120.100.200']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('CAR_DB_NAME'),
        'USER': env.str('CAR_DB_USER'),
        'PASSWORD': env.str('CAR_PASS'),
        'HOST': env.str('CAR_DB_HOST'),
        'PORT': env.str('CAR_DB_PORT'),
        # 'ATOMIC_REQUESTS': True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'filter_custom': {
            '()': 'core.log.UserFilter'
        }
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs/warnings.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['save_to_db', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# must be attach to real domain, smtp

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'carsharing@gmail.com'
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = 'CarSharing <carsharing@gmail.com>'
#
# ADMIN_EMAIL = 'admin@carsharing.ru'
