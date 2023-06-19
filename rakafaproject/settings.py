from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-d&-xg*yf+oe62#0h1l!bvlyurv&x#+xan#pvni=+wxee7eazg6'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [

    'rest_framework',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'api',
    # 'rakafaproject.celery',

    'site_setting',
    'site_admin',
    'site_account',
    'site_home',
    'site_product',
    'site_order',
    'site_form',
    'site_userpanel',
    'site_blog',

    'extra_views',
    'polls',
    'django_render_partial',
    'widget_tweaks',
    'jalali_date',
    'ckeditor',
    'ckeditor_uploader',
    'sorl.thumbnail',
    'robots',
    'validate_email',

    'throttle',
    'coupon_management',

]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rakafaproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'rakafaproject.wsgi.application'

AUTH_USER_MODEL = 'site_account.User'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'kcipcom_rakafa_project',
#         'USER': 'kcipcom_rakafa_project_user',
#         'PASSWORD': 'Taymazak114451445',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS':{
#             'sql_mode':'STRICT_ALL_TABLES'
#         }
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'static_cdn'
MEDIA_URL = '/medias/'
MEDIA_ROOT = BASE_DIR / 'uploads'
CKEDITOR_UPLOAD_PATH = "uploads/ckeditor/"

CKEDITOR_CONFIGS = {
    'default': {

        'toolbar': 'full',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'trotaymaz@gmail.com'
EMAIL_HOST_PASSWORD = 'dmrjzuslizeytzja'
EMAIL_PORT = 587

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'mail.pmaserver.cf'
# EMAIL_HOST_USER = 'info@pmaserver.cf'
# EMAIL_HOST_PASSWORD = 'Taymazak114451445'
# EMAIL_PORT = 587
# EMAIL_PORT = 465


THROTTLE_ZONES = {
    'default': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,  # Number of buckets worth of history to keep. Must be at least 2
        'BUCKET_INTERVAL': 15 * 60,  # Period of time to enforce limits.
        'BUCKET_CAPACITY': 50,  # Maximum number of requests allowed within BUCKET_INTERVAL
    },

    'basket_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2, 'BUCKET_INTERVAL': 1 * 60,
        'BUCKET_CAPACITY': 10,
    },

    'bookmark_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 1 * 60,
        'BUCKET_CAPACITY': 10,
    },

    'comments_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 50 * 60,
        'BUCKET_CAPACITY': 3,
    },

    'login_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 1 * 60,
        'BUCKET_CAPACITY': 15,
    },

    'resend_otp_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 1 * 60,
        'BUCKET_CAPACITY': 1,
    },

    'contact_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 10 * 60,
        'BUCKET_CAPACITY': 3,
    },

    'email_sign_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 60 * 60,
        'BUCKET_CAPACITY': 3,
    },

    'filter_product_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 1 * 20,
        'BUCKET_CAPACITY': 10,
    },

    'addresses_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 1 * 20,
        'BUCKET_CAPACITY': 5,
    },

    'change_order_count_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 1 * 20,
        'BUCKET_CAPACITY': 30,
    },

    'set_phone_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 2 * 60,
        'BUCKET_CAPACITY': 3,
    },

    'set_email_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 2 * 60,
        'BUCKET_CAPACITY': 10,
    },

    'use_coupon_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 1 * 30,
        'BUCKET_CAPACITY': 10,
    },
    'check_status_delay': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 2,
        'BUCKET_INTERVAL': 1 * 30,
        'BUCKET_CAPACITY': 10,
    },
}
# Optional after Redis backend is chosen ('throttle.backends.redispy.RedisBackend')
THROTTLE_REDIS_HOST = 'localhost'
THROTTLE_REDIS_PORT = 6379
THROTTLE_REDIS_DB = 0
THROTTLE_REDIS_AUTH = 'pass'

# Where to store request counts.
THROTTLE_BACKEND = 'throttle.backends.cache.CacheBackend'

# Force throttling when DEBUG=True
THROTTLE_ENABLED = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Tehran'
# CELERY_ENABLE_UTC = True

# CELERY_BROKER_URL = 'redis://:3sxhVLhoYpQSn7ZB1DC0yNeU@alfie.iran.liara.ir:32380/0'
# CELERY_RESULT_BACKEND = 'redis://:3sxhVLhoYpQSn7ZB1DC0yNeU@alfie.iran.liara.ir:32380/0'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Tehran'
# CELERY_ENABLE_UTC = True

# CELERY_BROKER_URL = 'redis://:fLO0biMrsJHL9ctbYWAtEsZs@alfie.iran.liara.ir:30232/0'
# CELERY_RESULT_BACKEND = 'redis://:fLO0biMrsJHL9ctbYWAtEsZs@alfie.iran.liara.ir:30232/0'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Tehran'
# CELERY_ENABLE_UTC = True

