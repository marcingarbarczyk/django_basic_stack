import socket

from .common import *  # noqa

# Debug toolbar

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())

INTERNAL_IPS = ['.'.join(ip.split('.')[:-1] + ['1']) for ip in ips] + ['127.0.0.1', '10.0.2.2']

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INSTALLED_APPS += ['debug_toolbar']

TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
]
