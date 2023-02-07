from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger,Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://admin:admin@localhost:5433/example_tele_bot", echo=True)

Base = declarative_base()


class Admins(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    admin_last_name = Column(String(50), nullable=False)
    admin_telegram_id = Column(BigInteger, nullable=False, unique=True)


class AllClient(Base):
    __tablename__ = 'allClient'

    id = Column(Integer, primary_key=True)
    client_id = Column(BigInteger, nullable=False, unique=True)


class CafeMenu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    photo_id = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric)


create_session = sessionmaker(bind=engine)
session = create_session()
