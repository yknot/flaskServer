#
#
# PRODUCTION config
#
#

import os


# database path
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
