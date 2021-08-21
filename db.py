from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import connection_db

# Local host
#connection_db = "postgresql://postgres:postgres@localhost:5433/flask_bd"
Base = declarative_base()

engine = create_engine(connection_db)

Session = sessionmaker(bind=engine)