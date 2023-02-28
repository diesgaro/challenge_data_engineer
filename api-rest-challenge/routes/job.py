from fastapi import APIRouter
from config.db import conn
from models.job import Jobs
from models.log import Logs
from schemas.job import Job

job = APIRouter()

@job.get('/jobs', response_model=list[Job], tags=["jobs"])
def get_jobs():
    select_jobs = conn.execute(Jobs.select())
    select_jobs_as_dict = select_jobs.mappings().fetchall()

    return select_jobs_as_dict

@job.post('/jobs', response_model=list[Job], tags=["jobs"])
def add_job(job: list[Job]):
    response = None
    if len(job) <= 1000:
        ls_new_job = []
        ls_fail_job = []

        for row in job:
            new_job = {}

            try:
                new_job['id'] = None
                new_job['job'] = row.job

                # Get the last id from challenge.jobs for set the new id
                query_get_last_id = conn.execute(Jobs.select().order_by(Jobs.c.id.desc()))
                new_job['id'] = query_get_last_id.first().id + 1
                query_get_last_id.close()

                ls_new_job.append(new_job)
                conn.execute(Jobs.insert().values(new_job))
                conn.commit()
            except:
                ls_fail_job.append(row.dict())

        for row in ls_fail_job:
            fail_job = {}

            fail_job['process'] = 'add_job'
            fail_job['object_sended'] = str(row)

            conn.execute(Logs.insert().values(fail_job))
            conn.commit()

        response = ls_new_job
    else:
        response = [{"message":"Only can process less than 1000 rows"}]

    return response