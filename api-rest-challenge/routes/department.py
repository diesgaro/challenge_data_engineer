from fastapi import APIRouter
from config.db import conn
from models.department import Departments
from models.log import Logs
from schemas.department import Department

department = APIRouter()

@department.get('/departments', response_model=list[Department], tags=["departments"])
def get_departments():
    select_departments = conn.execute(Departments.select())
    select_departments_as_dict = select_departments.mappings().fetchall()

    return select_departments_as_dict

@department.post('/departments', response_model=list[Department], tags=["departments"])
def add_department(department: list[Department]):
    response = None
    if len(department) <= 1000:
        ls_new_department = []
        ls_fail_department = []

        for row in department:
            new_department = {}

            try:
                new_department['id'] = None
                new_department['department'] = row.department

                # Get the last id from challenge.departments for set the new id
                query_get_last_id = conn.execute(Departments.select().order_by(Departments.c.id.desc()))
                new_department['id'] = query_get_last_id.first().id + 1
                query_get_last_id.close()

                ls_new_department.append(new_department)
                conn.execute(Departments.insert().values(new_department))
                conn.commit()
            except:
                ls_fail_department.append(row.dict())

        for row in ls_fail_department:
            fail_department = {}

            fail_department['process'] = 'add_department'
            fail_department['object_sended'] = str(row)

            conn.execute(Logs.insert().values(fail_department))
            conn.commit()

        response = ls_new_department
    else:
        response = [{"message":"Only can process less than 1000 rows"}]

    return response