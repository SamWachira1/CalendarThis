import os


class Config(object):
    # Property used by multiple Flask add-ons for security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-key-for-devs'
    DB_FILE = os.environ.get('DB_FILE') or 'dev.db'
