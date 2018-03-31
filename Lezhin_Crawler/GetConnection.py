from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import Constants

if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': Constants.ENGINE,
            'NAME': os.environ[Constants.NAME],
            'USER': os.environ[Constants.USER],
            'PASSWORD': os.environ[Constants.PASSWORD],
            'HOST': os.environ[Constants.HOST],
            'PORT': os.environ[Constants.PORT],
        }
    }
engine = create_engine(Constants.DB_URL)

conn = engine.connect()

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	Base.metadata.create_all(engine)
