from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import PendingRollbackError
# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://postgres:1054542694@localhost/soff_database"

POSTGRES_RENDER_URL = f"postgresql+psycopg2://evelyn:kXNpCO6LrjNZZj6W4c6J2FHJhkWTQaMU@dpg-cl7f5cavokcc73allfm0-a.oregon-postgres.render.com/soff_database_xzqf"

engine = create_engine(POSTGRES_RENDER_URL, pool_size=10, max_overflow=20)

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
      
  def rollback_on_pending_rollback(func):
    def wrapper(*arg, **kwargs):
      try:
        return func(*arg, **kwargs)
      except PendingRollbackError as e:
        ConectDatabase.getInstance().rollback
    return wrapper



# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from dotenv import dotenv_values


# values = dotenv_values('.env')

# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{values.get('USERNAME')}:{values.get('PASSWORD')}@{values.get('SERVER')}/soff_database"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base = declarative_base()

# class ConectDatabase:
#   __instance: SessionLocal = None
  
#   @staticmethod
#   def getInstance():
#     if ConectDatabase.__instance == None:
#       ConectDatabase()
#     return ConectDatabase.__instance
  
#   def __init__(self):
#     if ConectDatabase.__instance != None:
#       raise Exception("ConectDatabase exists already")
#     else:
#       ConectDatabase.__instance = SessionLocal()