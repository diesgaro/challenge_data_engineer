from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta

Departments = Table(
    'departments', 
    meta, 
    Column('id', Integer),
    Column('department', String(50)),
    schema='challenge'
)