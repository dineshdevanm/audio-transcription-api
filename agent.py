from faster_whisper import WhisperModel
import subprocess
import tempfile
import os
import time

print("Loading Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded")


def convert_to_wav(input_path):

    wav_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            wav_file.name
        ],
        capture_output=True,
        text=True
    )

    print("FFMPEG STDOUT:")
    print(result.stdout)

    print("FFMPEG STDERR:")
    print(result.stderr)

    if result.returncode != 0:
        raise Exception(f"FFmpeg failed: {result.stderr}")

    return wav_file.name


def transcribe_audio(audio_path):

    start_time = time.time()

    wav_path = convert_to_wav(audio_path)

    print("Starting transcription...")

    segments, info = model.transcribe(
        wav_path,
        beam_size=1,
        vad_filter=True
    )

    transcript = ""

    for segment in segments:
        transcript += segment.text + " "

    os.remove(wav_path)

    return {
        "detected_language": info.language,
        "transcript": transcript.strip(),
        "processing_time_seconds": round(
            time.time() - start_time,
            2
        )
    }