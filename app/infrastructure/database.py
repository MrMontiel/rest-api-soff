from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://postgres:1054542694@localhost/soff_database"

POSTGRES_RENDER_URL = f"postgresql+psycopg2://evelyn:kXNpCO6LrjNZZj6W4c6J2FHJhkWTQaMU@dpg-cl7f5cavokcc73allfm0-a.oregon-postgres.render.com/soff_database_xzqf"

engine = create_engine(
        POSTGRES_RENDER_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        connect_args={
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        })

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