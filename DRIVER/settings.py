"""
Django settings for DRIVER project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gzj9!(e96ak91gy0kdl%35t7z+uyd$)i%#mpnfe!ias3%aqs28'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEVELOP = True if os.environ.get('DJANGO_ENV', 'development') == 'development' else False
STAGING = True if os.environ.get('DJANGO_ENV', 'staging') == 'staging' else False
PRODUCTION = not DEVELOP and not STAGING
DEBUG = DEVELOP
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework.authtoken',
    'djangooidc',
    'storages',
    'corsheaders',
    'django_filters',

    'django_extensions',
    'rest_framework_gis',

    'grout',

    'driver_advanced_auth',
    'data',
    'black_spots',
    'user_filters',

    # allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # for google
    'allauth.socialaccount.providers.google',

    # 'django_celery_beat'
]

# old
HOST_URL =os.environ.get('HOST_URL')
SENDGRID_API_KEY = ''
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'ganeshghuge'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'ganesh.ghuge@aventior.com'
# EMAIL_BACKEND = 'sgbackend.SendGridBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = ''

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ['*']

GROUT = {
    # It is suggested to change this if you know that your data will be limited to
    # a certain part of the world, for example to a UTM Grid projection or a state
    # plane.
    'SRID': 4326,
}

ROOT_URLCONF = 'DRIVER.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# API HOST configuration
API_HOST = os.environ.get('HOST')

# APACHE server port
APACHE_PORT = '3200'

# redis configuration
REDIS_HOST = os.environ.get('DRIVER_REDIS_HOST')

REDIS_PORT = os.environ.get('DRIVER_REDIS_PORT')

# JAR file cache TLL (keep in redis for this many seconds since creation or last retrieval)
JARFILE_REDIS_TTL_SECONDS = os.environ.get('DRIVER_JAR_TTL_SECONDS', 60 * 60 * 24 * 30)  # 30 days

CACHES = {
    "default": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://' + REDIS_HOST + ':' + REDIS_PORT,
        'TIMEOUT': None,  # never expire
        'KEY_PREFIX': 'DJANGO',
        'VERSION': 1,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,  # seconds
            'SOCKET_TIMEOUT': 5,  # seconds
            'MAX_ENTRIES': 900,  # defaults to 300
            'CULL_FREQUENCY': 4,  # fraction culled when max reached (1 / CULL_FREQ); default: 3
            # 'COMPRESS_MIN_LEN': 0, # set to value > 0 to enable compression
        }
    },
    "jars": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/3',
        'TIMEOUT': JARFILE_REDIS_TTL_SECONDS,
        'KEY_PREFIX': None,
        'VERSION': 1,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,  # seconds
            'SOCKET_TIMEOUT': 5,  # seconds
            'MAX_ENTRIES': 300,  # defaults to 300
            'CULL_FREQUENCY': 4,  # fraction culled when max reached (1 / CULL_FREQ); default: 3
            # 'COMPRESS_MIN_LEN': 0, # set to value > 0 to enable compression
        }
    },
    "boundaries": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{host}:{port}/4'.format(host=REDIS_HOST, port=REDIS_PORT),
        # Timeout is set and renewed at the individual key level in data/filters.py
        'TIMEOUT': None,
        'KEY_PREFIX': 'boundary',
        'VERSION': 1,
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DRIVER_DB_NAME'),
        'HOST': os.environ.get('DRIVER_DB_HOST'),
        'PORT': os.environ.get('DRIVER_DB_PORT'),
        'USER': os.environ.get('DRIVER_DB_USER'),
        'PASSWORD': os.environ.get('DRIVER_DB_PASSWORD'),
        'CONN_MAX_AGE': 0,  # in seconds
        #'OPTIONS': {
         #   'sslmode': 'require'
        #}
    }
}
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Celery
BROKER_URL = 'redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://{}:{}/1'.format(REDIS_HOST, REDIS_PORT)
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ROUTES = {
    'black_spots.tasks.calculate_black_spots.calculate_black_spots': {'queue': 'taskworker'},
    'black_spots.tasks.get_segments.cleanup': {'queue': 'taskworker'},
    'black_spots.tasks.get_segments.create_segments_tar': {'queue': 'taskworker'},
    'black_spots.tasks.get_segments.get_segments_shp': {'queue': 'taskworker'},
    'black_spots.tasks.load_road_network.load_road_network': {'queue': 'taskworker'},
    'black_spots.tasks.load_blackspot_geoms.load_blackspot_geoms': {'queue': 'taskworker'},
    'black_spots.tasks.generate_training_input.get_training_noprecip': {'queue': 'taskworker'},
    'black_spots.tasks.generate_training_input.get_training_precip': {'queue': 'taskworker'},
    'data.tasks.remove_duplicates.remove_duplicates': {'queue': 'taskworker'},
    'data.tasks.export_csv.export_csv': {'queue': 'taskworker'},
    'data.tasks.fetch_record_csv.export_records': {'queue': 'taskworker'}
}
# This needs to match the proxy configuration in nginx so that requests for files generated
# by celery jobs go to the right place.
CELERY_DOWNLOAD_PREFIX = '/'
CELERY_EXPORTS_FILE_PATH = '/var/www/media'
export_csv_keyname = 'driverIncidentDetails'
Read_Only_group = "Public"
# Deduplication settings
DEDUPE_TIME_RANGE_HOURS = float(os.environ.get('DRIVER_DEDUPE_TIME_RANGE_HOURS', '12'))
# .001 ~= 110m
DEDUPE_DISTANCE_DEGREES = float(os.environ.get('DRIVER_DEDUPE_DISTANCE_DEGREES', '0.0008'))

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TIMEZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT')

READ_ONLY_FIELDS_REGEX = r'Details$'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {

        'error_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'formatter': 'verbose'
        },

    },
    'loggers': {
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# this setting ensures celery will retry if broker is not immediately available when celery worker starts.
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# number of celery retries connecting to broker(redis in our case) before giving up.
CELERY_BROKER_CONNECTION_MAX_RETRIES = 5

#  duration in seconds between each retry
CELERY_BROKER_CONNECTION_RETRY_DELAY = 2

# to specify default auto field type, BigAutoField will be scalable moving ahead.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
