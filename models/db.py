from db.connection import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func

class Users(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True)
    password = Column(String)


class Empresa(Base):
    __tablename__ = "empresa"
    id = Column(Integer, primary_key=True, autoincrement=True)
    numeroRegistro = Column(String(14))
    nombre = Column(String(255))
    tipo = Column(String(255))
    correo = Column(String(255))
    contrasenia = Column(String(255))
    numTelefono = Column(String(20))
    pais = Column(String(50))
    region = Column(String(50))
    direccion = Column(String(300))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

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