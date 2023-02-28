from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta

Jobs = Table(
    'jobs', 
    meta, 
    Column('id', Integer),
    Column('job', String(50)),
    schema='challenge'
)