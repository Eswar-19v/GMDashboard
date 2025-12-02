from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aggregators import fetch_sprint_tasks, fetch_qa_tasks, fetch_prod_escalations,fetch_all_data
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all UI origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/sprint-tasks")
def get_sprint_tasks():
    return fetch_sprint_tasks()

@app.get("/qa-tasks")
def get_qa_tasks():
    return fetch_qa_tasks()

@app.get("/production-escalations")
def get_production_escalations():
    return fetch_prod_escalations()

class SprintData(BaseModel):
    sprintnumber: int

@app.post("/get_data")
def get_data(data: SprintData):
    return fetch_all_data(data.sprintnumber)
    

    
