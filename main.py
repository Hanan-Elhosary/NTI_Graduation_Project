from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from run_crew import crew

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "\ud83d\ude80 FastAPI Backend Ready"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

class CrewInput(BaseModel):
    argument: str
    csv_path: Optional[str] = None

@app.post("/run-crew")
async def run_crew_endpoint(data: CrewInput):
    result = crew.run(data.dict())
    return {"result": result}
