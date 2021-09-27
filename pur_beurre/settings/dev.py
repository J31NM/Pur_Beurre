from pur_beurre.settings.base import *

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar', ]
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    TEMPLATES[0]["OPTIONS"]["context_processors"].insert(0, 'django.template.context_processors.debug')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pur_beurre_db',
        'USER': 'postgres',
        # 'PASSWORD': os.environ.get("PASSWORD"),
        'PASSWORD': "H3kth@r6819",
        'HOST': 'localhost',
        'PORT': '5433',
    }
}