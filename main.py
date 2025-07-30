from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow Frontend (Streamlit) to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "🚀 FastAPI Backend Ready"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

# Entry point to run the app directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
