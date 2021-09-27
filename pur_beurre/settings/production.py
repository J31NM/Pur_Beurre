from pur_beurre.settings.base import *

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

