from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

user=os.environ.get("DATABASE_USERNAME")
password=os.environ.get("DATABASE_PASSWORD")
database = os.environ.get("DATABASE")
host=os.getenv("DATABASE_HOST")

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{username}@{host}/{database}" # or "mysql+pymysql://db_username:user_password@localhost/test"
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}/{database}" # or "mysql+pymysql://db_username:user_password@localhost/test"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost/test" # or "mysql+pymysql://db_username:user_password@localhost/test"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # , connect_args={"check_same_thread": False} # only for sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()