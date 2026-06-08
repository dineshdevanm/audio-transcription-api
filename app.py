from fastapi import FastAPI, UploadFile
from agent import transcribe_audio
import shutil
import os
import shutil

os.makedirs("uploads", exist_ok=True)

file_path = f"uploads/{file.filename}"

with open(file_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)

app = FastAPI()

@app.post("/transcribe")
async def transcribe(file: UploadFile):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = transcribe_audio(file_path)

    return result



@app.get("/")
def home():
    return {
        "version": "NEW_VERSION_123"
    }