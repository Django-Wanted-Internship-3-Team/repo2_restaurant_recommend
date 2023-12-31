import os
from datetime import timedelta
from pathlib import Path

import environ

from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, True))

environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", default="test")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = ["*"]

# Application definition
THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_yasg",
    "django_apscheduler",
]

LOCAL_APPS = [
    "restaurants_recommendation.users.apps.UsersConfig",
    "restaurants_recommendation.common.apps.CommonConfig",
    "restaurants_recommendation.restaurants.apps.RestaurantsConfig",
    "restaurants_recommendation.reviews.apps.ReviewsConfig",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.root_urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRESQL_DATABASE", default="repo_2"),
        "USER": env("POSTGRESQL_USER", default="postgres"),
        "PASSWORD": env("POSTGRESQL_PASSWORD", default="password"),
        "HOST": env("POSTGRESQL_HOST", default="localhost"),
        "PORT": env("POSTGRESQL_PORT", default="5432"),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator", "option": {"user_attributes": "username"}},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "option": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

# Swagger settings
SWAGGER_SETTINGS = {"SECURITY_DEFINITIONS": {"Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}}}

# DRF settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": ("djangorestframework_camel_case.render.CamelCaseJSONRenderer",),
    "DEFAULT_PARSER_CLASSES": ("djangorestframework_camel_case.parser.CamelCaseJSONParser",),
}


# Logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "django.server": {
            "format": "[%(asctime)s] %(levelname)s [PID: %(process)d - %(processName)s] | [TID: %(thread)d - %(threadName)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "django.server",
        },
        "file": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "django.server",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        }
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "ALGORITHM": "HS256",
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("REDIS_URL", default="redis://localhost:6379"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Celery
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://redis:6379/1")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default="redis://redis:6379/2")
CELERY_BEAT_SCHEDULE = {
    "demo-scheduled-task": {
        "task": "restaurants_recommendation.users.tasks.recommend_restaurants_to_user",
        "schedule": crontab(hour=12, day_of_week="mon-fri"),  # weekday at 12pm
    }
}

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

SCHEDULER_DEFAULT = True
