from faster_whisper import WhisperModel
import time

def transcribe_audio(audio_path):

    start_time = time.time()

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    segments, info = model.transcribe(audio_path)

    text = ""

    for segment in segments:
        text += segment.text + " "

    end_time = time.time()

    processing_time = round(end_time - start_time, 2)

    return {
        "transcript": text.strip(),
        "processing_time_seconds": processing_time
    }