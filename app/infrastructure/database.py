from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values


values = dotenv_values('.env')

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{values.get('USERNAME')}:{values.get('PASSWORD')}@{values.get('SERVER')}/soff_database"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

class ConectDatabase:
  __instance: SessionLocal = None
  
  @staticmethod
  def getInstance():
    if ConectDatabase.__instance == None:
      ConectDatabase()
    return ConectDatabase.__instance
  
  def __init__(self):
    if ConectDatabase.__instance != None:
      raise Exception("ConectDatabase exists already")
    else:
      ConectDatabase.__instance = SessionLocal()