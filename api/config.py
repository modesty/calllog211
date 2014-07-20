import os
from datetime import datetime
from google.appengine.api import app_identity

APPLICATION_ID = app_identity.get_application_id()

CURRENT_VERSION_ID = os.environ.get('CURRENT_VERSION_ID')
CURRENT_VERSION_NAME = CURRENT_VERSION_ID.split('.')[0]
CURRENT_VERSION_TIMESTAMP = long(CURRENT_VERSION_ID.split('.')[1]) >> 28
CURRENT_VERSION_DATE = datetime.fromtimestamp(CURRENT_VERSION_TIMESTAMP)

PRODUCTION = os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Eng')
DEVELOPMENT = True #not PRODUCTION
DEBUG = DEVELOPMENT

API_ROUTE_ROOT = '/api/v1.0/{0}/{1}'

# 1 hour session time span
SESSION_TIME_SPAN=3600

# import model
#
# CONFIG_DB = model.Config.get_master_db()
# SECRET_KEY = CONFIG_DB.flask_secret_key.encode('ascii')

DEFAULT_DB_LIMIT = 64
