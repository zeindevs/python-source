import logging
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, String, Integer, DateTime, Text
from sqlalchemy.orm import sessionmaker


logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
logging.getLogger("pyodbc").setLevel(logging.DEBUG)

DB_USER = ""
DB_PASS = ""
DB_NAME = "HRScrapper"
DB_HOST = "(localdb)\\MSSQLLocalDB"
DSN = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?"
    "driver=ODBC+Driver+18+for+SQL+Server"
)

engine = create_engine(DSN, echo=False)
metadata = MetaData()

tb_offer = Table(
    "tb_offer",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100)),
    Column("description", String(100)),
    Column("location", Text),
    Column("sallary", Integer, nullable=True),
    Column("expires_at", DateTime, nullable=True),
)

Session = sessionmaker(bind=engine)
session = Session()
