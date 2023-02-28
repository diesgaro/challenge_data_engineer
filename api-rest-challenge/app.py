from fastapi import FastAPI
from routes.employee import employee
from routes.department import department
from routes.job import job

app = FastAPI(
    title="API Challenge #1",
    description="Rest API Service that receive new data about employees, departments and jobs",
    version='0.0.1',
    openapi_tags=[{
        "name":"employees",
        "description":"employees routes"
    },{
        "name":"departments",
        "description":"departments routes"
    },{
        "name":"jobs",
        "description":"jobs routes"
    }]
)

app.include_router(employee)
app.include_router(department)
app.include_router(job)

@app.get('/')
def root():
    return {"Mesagge":"API Challenge #1"}