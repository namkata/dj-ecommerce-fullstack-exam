from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')  # noqa: F405

# Use WhiteNoise for serving static files in production
INSTALLED_APPS.insert(1, 'whitenoise.runserver_nostatic')  # noqa: F405

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa: F405

# Security Settings
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(ROOT_DIR, 'logs', 'django_error.log'),  # noqa: F405
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Database Connection Pooling (Optional)
DATABASES['default']['CONN_MAX_AGE'] = 600  # noqa: F405
