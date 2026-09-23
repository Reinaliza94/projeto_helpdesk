from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

DB_SERVER_URL = "mysql+pymysql://root:@localhost"
DATABASE_URL = "mysql+pymysql://root:@localhost/test"

server_engine = create_engine(DB_SERVER_URL, echo=True)
with server_engine.begin() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS test"))

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)