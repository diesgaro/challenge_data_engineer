#import pyodbc
from sqlalchemy import create_engine, MetaData

dialect = 'mssql'
driver = 'pyodbc'
username = 'user_synapse'
password = '0tk*aYtEVEzz'
host = 'sql-server-onb-demo.database.windows.net'
port = '1433'
database = 'db-sql-onb-demo'

string_connection = "{}+{}://{}:{}@{}:{}/{}?driver=ODBC+Driver+18+for+SQL+Server".format(
    dialect,driver,username,password,host,port,database)

engine = create_engine(string_connection)

meta = MetaData()

conn = engine.connect()