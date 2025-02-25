"""
Django settings for ecom project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_DIR = BASE_DIR.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'foo'
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # Should be overridden in development.py
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# Application definition
INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # If using Django REST Framework
    'corsheaders',     # If using CORS headers

    # My App (Using startapp commands)
    'core',
    'auths',
    'apps.categories',
    'apps.products',
    'apps.abouts',
    'apps.orders',
    'apps.reviews',
    'apps.payments',
    'apps.contacts',
    'apps.shipping',
    'apps.promotions',
    'apps.analytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # If using CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.categories.context_processors.categories_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/staticfiles/'
# Thư mục gốc chứa các tệp tĩnh (chỉ sử dụng khi DEBUG=False)
STATIC_ROOT = os.path.join(ROOT_DIR, "staticfiles")

# STATICFILES_DIRS = [
#     ROOT_DIR  / "staticfiles/",
# ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, "media")

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STORAGES = {
     "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_ROOT,  # Đường dẫn lưu file
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        "OPTIONS": {
            "location": STATIC_ROOT,  # Thư mục lưu static
        },
    },
    # Các cấu hình khác...
}


REQUIRED_DIRS = [
    os.path.join(ROOT_DIR, "logs"),
    os.path.join(ROOT_DIR, "locales"),
]

for directory in REQUIRED_DIRS:
    os.makedirs(directory, exist_ok=True)

LOCALE_PATHS = [
    os.path.join(ROOT_DIR, "logs"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'auths.User'

# Configure
GRAPPELLI_ADMIN_HEADLINE = 'E-commerce administration'
GRAPPELLI_ADMIN_TITLE = 'E-commerce administration'
GRAPPELLI_AUTOCOMPLETE_LIMIT=10
ADMIN_URL = os.getenv("ADMIN_URL", "admin/")
GRAPPELLI_ADMIN_URL=ADMIN_URL
