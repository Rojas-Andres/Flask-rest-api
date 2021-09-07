from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from config import connection_db

# Local host
connection_db = "sqlite:///basedatos.db"
Base = declarative_base()

engine = create_engine(connection_db)

Session = sessionmaker(bind=engine)