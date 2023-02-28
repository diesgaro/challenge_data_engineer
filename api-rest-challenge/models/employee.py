from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
#from sqlalchemy.sql.expression import exists
from config.db import meta

Employees = Table(
    'employees', 
    meta, 
    Column('id', Integer),
    Column('name', String(50)),
    Column('date', Integer),
    Column('time', String(8)),
    Column('department_id', Integer),
    Column('job_id', Integer),
    schema='challenge'
)