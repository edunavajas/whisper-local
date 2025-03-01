import os
import tempfile
import whisper
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Whisper API", description="API para transcripción de audio usando Whisper")

# Cargar el modelo al inicio (puedes cambiarlo a "base", "small", "medium" o "large" según necesites)
model = None

@app.on_event("startup")
async def startup_event():
    global model
    print("Cargando modelo Whisper...")
    model = whisper.load_model("base")
    print("Modelo cargado correctamente!")

@app.post("/transcribe/", response_class=JSONResponse)
async def transcribe_audio(file: UploadFile = File(...), language: str = None):
    """
    Transcribe un archivo de audio usando Whisper.
    - **file**: Archivo de audio a transcribir (formatos soportados: mp3, wav, m4a, etc.)
    - **language**: Código de idioma opcional (es, en, fr, etc.)
    """
    if not file.filename.endswith(('.mp3', '.wav', '.m4a', '.ogg', '.flac')):
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado")

    # Guardar archivo temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp:
        try:
            # Escribir contenido del archivo
            content = await file.read()
            temp.write(content)
            temp.flush()
            
            # Configurar opciones de transcripción
            transcribe_options = {}
            if language:
                transcribe_options["language"] = language
            
            # Realizar transcripción
            result = model.transcribe(temp.name, **transcribe_options)
            
            return {
                "text": result["text"],
                "segments": result["segments"],
                "language": result["language"]
            }
        
        finally:
            # Limpiar archivo temporal
            os.unlink(temp.name)

@app.get("/health/")
def health_check():
    """Verificar que el servicio está funcionando"""
    return {"status": "ok", "model_loaded": model is not None}