# Settings for the "development" environment.
from project.settings.base import *

DJANGO_ENV = "development"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '../development.sqlite3',
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
)

INTERNAL_IPS = (
    '127.0.0.1',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

MIDDLEWARE_CLASSES += (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)
