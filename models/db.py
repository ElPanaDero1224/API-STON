from db.connection import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey

class Users(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True)
    password = Column(String)

class Products(Base):
    __tablename__ = "inventario"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String)
    barcode = Column(Integer)
    quantity = Column(Integer)
    expiration_dates = Column(JSON)

class Statistics(Base):
    __tablename__ = "estadisticas"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    product_id = Column(Integer, ForeignKey("inventario.id"))
    action = Column(String)
    date = Column(String)