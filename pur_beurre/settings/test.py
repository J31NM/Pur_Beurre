from pur_beurre.settings.base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # 'postgresql', 'mysql', 'sqlite3', 'oracle'.
        'NAME': os.path.join(BASE_DIR, '../../pur_beurre_test.db'),
    },
}
