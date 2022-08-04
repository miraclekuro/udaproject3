import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="uadproject3dbserver.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="udaadmin@uadproject3dbserver" #TODO: Update value
    POSTGRES_PW="Matkhaulan#1"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://udaproject3bus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=5uSCo6H67JsTk+k6mCA5zT6RIu+rqwifngevsjjF2iM=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notification'
    ADMIN_EMAIL_ADDRESS: 'miracle15794@gmail.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False