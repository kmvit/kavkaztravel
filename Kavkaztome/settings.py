"""
Django settings for Kavkaztome project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get("SECRET_KEY", default=get_random_secret_key())
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = os.environ.get("HOST", default="127.0.0.1, localhost").split(",")
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "djoser",
    "core",
    "users",
    "regions",
    "hotels",
    "restaurants",
    "tours",
    "entertainments",
    "drf_spectacular",
    "drf_spectacular_sidecar",  # required for Django collectstatic discovery
    "oauth2_provider",
    "social_django",
    "rest_framework_social_oauth2",
    "blog",
    "kashiring",
    "sms",
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

ROOT_URLCONF = "Kavkaztome.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "Kavkaztome.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",  # django-oauth-toolkit >= 1.0.0
        "drf_social_oauth2.authentication.SocialAuthentication",
    ],
    #'DEFAULT_PERMISSION_CLASSES': [
    #    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    # ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

AUTHENTICATION_BACKENDS = (
    "social_core.backends.vk.VKOAuth2",
    "drf_social_oauth2.backends.DjangoOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SPECTACULAR_SETTINGS = {
    "TITLE": "KAVKAZ API",
    "DESCRIPTION": "Сервис для жизни на Кавказе",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    # -------- Нужно, чтобы раздавать статику для Swagger локально --------
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    # ---------------------------------------------------------------------
}

SOCIAL_AUTH_VK_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_VK_OAUTH2_KEY")  #'51471973'
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ.get(
    "SOCIAL_AUTH_VK_OAUTH2_SECRET"
)  #'0HKCRPAiifvxIdalGD01'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=500),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=50),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# Нстройки для авторизации через Email c использованием библиотеки DJOSER
DJOSER = {
    "USER_ID_FIELD": "username",
    "LOGIN_FIELD": "email",
    "SEND_ACTIVATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SERIALIZERS": {},
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SITE_NAME = "SaaSitive"


# Настройки для авторизации через телефон смс
# Настройки для SMS.py
SMS_API_KEY = os.environ.get("SMS_API_KEY")
SMS_API_URL = "https://api.smsprovider.com/send_sms"
