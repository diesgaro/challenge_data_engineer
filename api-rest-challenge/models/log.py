from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta

Logs = Table(
    'logs', 
    meta, 
    Column('id', Integer),
    Column('process', String(50)),
    Column('object_sended', String(1000)),
    schema='challenge'
)