from sqlalchemy import Column, ForeignKey, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, unique=True)


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, unique=True)


class Orders(Base):
    __tablename__ = 'orders'
    order_number = Column(Integer, primary_key=True)
    order_line_number = Column(Integer, primary_key=True)
    quantity_ordered = Column(Integer)
    price_each = Column(Float)
    sales = Column(Float)

    status_id = Column(Integer, ForeignKey('status.id'))
    status = relationship(Status)

    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship(Country)








