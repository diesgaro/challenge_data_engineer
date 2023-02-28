from fastapi import APIRouter
from config.db import conn
from models.employee import Employees, Employees_by_quarter, Employees_by_department
from models.department import Departments
from models.job import Jobs
from models.log import Logs
from schemas.employee import Employee, Employee_by_quarter, Employee_by_department

employee = APIRouter()

@employee.get('/employees', response_model=list[Employee], tags=["employees"])
def get_employees():
    select_employees = conn.execute(Employees.select())
    select_employees_as_dict = select_employees.mappings().fetchall()

    select_employees.close()

    return select_employees_as_dict
    #return conn.execute()

@employee.post('/employees', response_model=list[Employee], tags=["employees"])
def add_employee(employee: list[Employee]):
    response = None
    if len(employee) <= 1000:
        ls_new_employees = []
        ls_fail_employees = []

        for row in employee:
            new_employee = {}

            try:
                new_employee['id'] = row.id
                new_employee['name'] = row.name
                new_employee['date'] = row.datetime.split('T')[0].replace('-','')
                new_employee['time'] = row.datetime.split('T')[1].replace('Z','')
                new_employee['department_id'] = row.department_id
                new_employee['job_id'] = row.job_id

                # Get the last id from challenge.empoyees for set the new id
                query_get_last_id = conn.execute(Employees.select().order_by(Employees.c.id.desc()))
                new_employee['id'] = query_get_last_id.first().id + 1
                query_get_last_id.close()

                # Validate if department exist
                query_validate_department = conn.execute(Departments.select().where(Departments.c.id == row.department_id))
                department_valid = True if query_validate_department.first() else False
                query_validate_department.close()

                # Validate if job exist
                query_validate_job = conn.execute(Jobs.select().where(Jobs.c.id == row.job_id))
                job_valid = True if query_validate_job.first() else False
                query_validate_job.close()

                if department_valid and job_valid:
                    #print(new_employee)
                    ls_new_employees.append(new_employee)
                    conn.execute(Employees.insert().values(new_employee))
                    conn.commit()
                else:
                    ls_fail_employees.append(row.dict())
            except:
                ls_fail_employees.append(row.dict())

        for row in ls_fail_employees:
            fail_employee = {}

            fail_employee['process'] = 'add_employee'
            fail_employee['object_sended'] = str(row)

            conn.execute(Logs.insert().values(fail_employee))
            conn.commit()

        response = ls_new_employees
    else:
        response = [{"message":"Only can process less than 1000 rows"}]

    return response

@employee.get('/employees_by_quarter',response_model=list[Employee_by_quarter], tags=["employees"])
def get_employees_by_quarter():
    select_employees_by_quarter = conn.execute(Employees_by_quarter.select().order_by(Employees_by_quarter.c.department.asc(),Employees_by_quarter.c.job.asc()))
    select_employees_by_quarter_as_dict = select_employees_by_quarter.mappings().fetchall()

    select_employees_by_quarter.close()

    return select_employees_by_quarter_as_dict

@employee.get('/employees_by_department',response_model=list[Employee_by_department], tags=["employees"])
def get_employees_by_department():
    select_employees_by_department = conn.execute(Employees_by_department.select().order_by(Employees_by_department.c.hired.desc()))
    select_employees_by_department_as_dict = select_employees_by_department.mappings().fetchall()

    select_employees_by_department.close()

    return select_employees_by_department_as_dict