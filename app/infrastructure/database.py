from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://postgres:letmain@localhost/soff_database"

POSTGRES_RENDER_URL = f"postgresql+psycopg2://ldmontiel:pHQ3Zl9ekNaYtp231yRg0ow0W2KgMzey@dpg-cl07nojjdq6s73aj5i30-a.oregon-postgres.render.com/soff"

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