import os
import tempfile
import subprocess
import whisper
from fastapi import FastAPI, UploadFile, File, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Whisper API", description="API for audio transcription using Whisper")

# Configuración de autenticación
API_KEY = os.getenv("API_KEY", "")
api_key_header = APIKeyHeader(name="X-API-Key")

# Función para verificar la API key
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Could not validate API key"
        )
    return api_key_header

model = None

VIDEO_FORMATS = ('.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.wmv')
AUDIO_FORMATS = ('.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.wma', '.opus', '.amr')
ALL_FORMATS = VIDEO_FORMATS + AUDIO_FORMATS

@app.on_event("startup")
async def startup_event():
    global model
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    print("Model loaded successfully!")

@app.post("/transcribe/", response_class=JSONResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = None,
    api_key: str = Depends(get_api_key)
):
    """
    Transcribe an audio or video file using Whisper.
    - **file**: File to be transcribed (audio or video)
    - **language**: Optional language code (es, en, fr, etc.)
    Requires API key authentication in X-API-Key header
    """
    file_extension = os.path.splitext(file.filename.lower())[1]
    if file_extension not in ALL_FORMATS:
        raise HTTPException(
            status_code=400, 
            detail=f"Format {file_extension} not supported. Supported formats: {', '.join(ALL_FORMATS)}"
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_input:
        try:
            content = await file.read()
            temp_input.write(content)
            temp_input.flush()
            input_path = temp_input.name

            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_output:
                output_path = temp_output.name

            print(f"Converting file {file.filename} to WAV format for processing...")
            try:
                subprocess.run([
                    'ffmpeg', 
                    '-y',
                    '-i', input_path,
                    '-af', 'silenceremove=stop_threshold=-50dB:stop_duration=1:stop_periods=-1',  #Delete silences
                    '-ar', '16000',
                    '-ac', '1',
                    '-c:a', 'pcm_s16le',
                    output_path
                ], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="Error processing file. Ensure it is a valid audio or video file."
                )

            options = {}
            if language:
                options["language"] = language

            print("Transcribing audio...")
            result = model.transcribe(output_path, **options)
            print("Transcription completed.")

            return {
                "text": result["text"],
                "segments": result["segments"],
                "language": result["language"],
                "original_filename": file.filename
            }

        finally:
            try:
                if os.path.exists(input_path):
                    os.unlink(input_path)
                if os.path.exists(output_path):
                    os.unlink(output_path)
            except Exception as e:
                print(f"Error removing temporary files: {e}")

@app.get("/health/")
def health_check(api_key: str = Depends(get_api_key)):
    """Check if the service is running"""
    return {"status": "ok", "model_loaded": model is not None}

@app.get("/formats/")
def supported_formats(api_key: str = Depends(get_api_key)):
    """List supported formats"""
    return {
        "video_formats": VIDEO_FORMATS,
        "audio_formats": AUDIO_FORMATS
    }
