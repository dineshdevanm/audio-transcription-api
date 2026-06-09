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
    try:
        import tempfile
        import shutil
        import os

        print("Received:", file.filename)

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(file.filename)[1]
        )
        temp_file.close()

        with open(temp_file.name, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("Saved:", temp_file.name)

        result = transcribe_audio(temp_file.name)

        print("Done")

        return result

    except Exception as e:
        import traceback

        error = traceback.format_exc()

        print(error)

        return {
            "error": str(e),
            "traceback": error
        }