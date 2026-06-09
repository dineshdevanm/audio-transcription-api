from fastapi import FastAPI, UploadFile, File
from agent import transcribe_audio
import tempfile
import shutil
import os

app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Audio Transcription API"
    }

@app.get("/debug")
def debug():
    return {
        "status": "ok",
        "version": "v2"
    }

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(file.filename)[1]
    )
    temp_file.close()
    with open(temp_file.name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        try:
            result = transcribe_audio(temp_file.name)
            return result

        except Exception as e:
            import traceback

            print("ERROR OCCURRED:")
            print(traceback.format_exc())

            return {
            "error": str(e)}

    finally:
        try:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)
        except Exception as e:
            print("Cleanup error:", e)