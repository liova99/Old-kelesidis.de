import MySQLdb
#local password file
from app.passwords import *
import os

DEBUG = True

# Define the application directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
#MySQL connection
def connection():
    conn = MySQLdb.connect(host= host,
                           user = user ,
                           passwd = passwd,
                           db = db)
    c = conn.cursor()
    return c, conn

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = CSRF_KEY

# Secret key for signing cookies
SECRET_KEY = SECRET_KEY