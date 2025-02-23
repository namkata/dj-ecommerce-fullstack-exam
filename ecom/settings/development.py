from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS += ['debug_toolbar']  # Django Debug Toolbar for dev  # noqa: F405

MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405

# Email Backend for Development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS settings (optional)
CORS_ALLOW_ALL_ORIGINS = True
