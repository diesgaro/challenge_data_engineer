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

Employees_by_quarter = Table(
    'employees_hired_by_quarter',
    meta,
    Column('department', String(50)),
    Column('job', String(50)),
    Column('Q1', Integer),
    Column('Q2', Integer),
    Column('Q3', Integer),
    Column('Q4', Integer),
    schema='challenge'
)

Employees_by_department = Table(
    'employees_hired_by_department',
    meta,
    Column('id', Integer),
    Column('department', String(50)),
    Column('hired', Integer),
    schema='challenge'
)