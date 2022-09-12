# https://towardsdatascience.com/fastapi-cloud-database-loading-with-python-1f531f1d438a
import sqlalchemy
from sqlalchemy import BigInteger, Integer, Column, DateTime, String
from database.db import Base

metadata = sqlalchemy.MetaData()


class Account(Base):
    __tablename__ = "t_accounts"
    id_account = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50))
    balance = Column(Integer)
    tstamp = Column(DateTime)
