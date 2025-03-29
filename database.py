from databases import Database
from sqlalchemy import MetaData
from decouple import config


DATABASE_URL = config("DATABASE_URL")  # Carga desde .env

database = Database(DATABASE_URL)
metadata = MetaData()
