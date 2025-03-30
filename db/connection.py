import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dbType = os.getenv('DB_TYPE')
dbName= os.getenv('DB_NAME')
dbUser= os.getenv('DB_USER')
dbPassword= os.getenv('DB_PASSWORD')
dbHost= os.getenv('DB_HOST')
dbPort= os.getenv('DB_PORT')

print(dbType, dbName, dbUser, dbPassword, dbHost, dbPort)

if dbType=="sqlite3":
    base_dir= os.path.dirname(os.path.realpath(__file__))
    dbURL= f"sqlite:///{os.path.join(base_dir,dbName)}"

if dbType=="mysql":
    dbURL= f"mysql+pymysql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbName}"

if dbType=="postgresql":
    dbURL= f"postgresql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbName}"

engine=create_engine(dbURL,echo=True)
Session=sessionmaker(bind=engine)
Base=declarative_base()