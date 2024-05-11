from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

#we pass the settings to our SQLALCHEMY_DATABASE_URL by Env variables
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
#postgresql://username:password@hostname:port/database_name
#postgresql://postgres:venezuela10@localhost:5432/fastapi
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#-----------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
#--------------------------------------------------------------------------------------------------------------------
"""
import psycopg2
from psycopg2.extras import RealDictCursor #To see the column
from time import time
    while True:

    try:
        conn = psycopg2.connect(host="localhost",#using local host
                                database="fastapi",#name of my DB
                                user="postgres",#Using postgres user
                                password="venezuela10",
                                cursor_factory=RealDictCursor)#To see the column
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except psycopg2.OperationalError as error:
        print("Operational Error: ", error)
    except psycopg2.ProgrammingError as error:
        print("Programming Error: ", error)
    except psycopg2.Error as error:
        print("Database Error: ", error)
        time.sleep(3)"""