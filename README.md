Whisper API - Lightweight Version
==================================

Overview:
---------
This is a lightweight version of Whisper designed to run locally or on any server using Docker.
It provides an API for transcribing audio files using the Whisper model and returns detailed segmentation
information along with the transcription result.

Features:
---------
- Lightweight transcription service based on Whisper.
- Deployable locally or on any server using Docker.
- Detailed segmentation data for advanced transcription analysis.

Installation and Deployment:
-----------------------------
1. Build the Docker image:
``` bash
   docker-compose build
  ``` 

2. Start the service in detached mode:
```bash
   docker-compose up -d
```

API Endpoints:
--------------
Health Check:
  - You can verify that the service is running by checking the health endpoint:
  ```bash
    curl http://localhost:8000/health/
```

Swagger Documentation:
  - View the interactive API documentation at:
    http://localhost:8000/docs

Transcription:
--------------
To call the transcription endpoint, use the following examples:

For a Spanish file:
```bash
  curl -X POST http://localhost:8000/transcribe/ \
    -H "Content-Type: multipart/form-data" \
    -F "file=@path/to/your/file.mp3" \
    -F "language=es"
 ```   

```bash
For any language (automatic detection):
  curl -X POST http://localhost:8000/transcribe/ \
    -H "Content-Type: multipart/form-data" \
    -F "file=@path/to/your/file.mp3"
```    

Explanation of Results:
-----------------------
The API returns a JSON object that includes:
- **text**: The full transcription of the audio.
- **segments**: An array of segments, each providing detailed information such as:
  - **start** and **end**: Timestamps (in seconds) indicating the start and end of the segment.
  - **text**: The transcribed text for that particular segment.
  - **tokens**: The token IDs processed by the model.
  - Additional metadata like `temperature`, `avg_logprob`, `compression_ratio`, and `no_speech_prob`
    that help evaluate the quality and confidence of the transcription.
- **language**: The detected or specified language of the audio.

The segmentation allows for precise alignment of text with the audio timeline, which is useful for subtitle generation,
quality assessment, or further processing of specific parts of the transcription.

