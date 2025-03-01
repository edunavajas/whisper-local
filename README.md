# Simple Whisper API

## Overview:

This is a lightweight version of Whisper designed to run locally or on any server using Docker. It provides an API for transcribing audio files using the Whisper model and returns detailed segmentation information along with the transcription result.

## Security:

This API requires an API key for authentication. Before running the service, you need to create a `.env` file in the root directory with the following content:

```bash
API_KEY=YOUR_GENERATED_API_KEY
```
You can generate via 

```bash
openssl rand -hex 32
```

This API key will be required in all requests using the `X-API-Key` header. This is a simple and fast way to add security without using a database. It is not the most ideal solution, but it provides basic security while keeping things lightweight.

## Features:

- Lightweight transcription service based on Whisper.
- Deployable locally or on any server using Docker.
- Simple API key authentication for security.
- Detailed segmentation data for advanced transcription analysis.

## Installation and Deployment:

1. Clone the repository:

   ```bash
   git clone https://github.com/edunavajas/whisper-local
   cd whisper-api
   ```

2. Create the `.env` file with an API key:

   ```bash
   echo "API_KEY=YOUR_GENERATED_API_KEY" > .env
   ```

3. Build the Docker image:

   ```bash
   docker-compose build
   ```

4. Start the service in detached mode:

   ```bash
   docker-compose up -d
   ```

## API Endpoints:

Health Check:

- Verify that the service is running by checking the health endpoint:

```bash
  curl -H "X-API-Key: YOUR_GENERATED_API_KEY" http://localhost:8000/health/
```

Formats:

- See the available file formats:

```bash
  curl -H "X-API-Key: YOUR_GENERATED_API_KEY" http://localhost:8000/formats/
```

Swagger Documentation:

- View the interactive API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Transcription:

To call the transcription endpoint, you must include the API key in the `X-API-Key` header:

For a Spanish file:

```bash
  curl -X POST http://localhost:8000/transcribe/ \
    -H "X-API-Key: YOUR_GENERATED_API_KEY" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@path/to/your/file.mp3" \
    -F "language=es"
```

For any language (automatic detection):

```bash
  curl -X POST http://localhost:8000/transcribe/ \
    -H "X-API-Key: YOUR_GENERATED_API_KEY" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@path/to/your/file.mp3"
```

## Explanation of Results:

The API returns a JSON object that includes:

- **text**: The full transcription of the audio.
- **segments**: An array of segments, each providing detailed information such as:
  - **start** and **end**: Timestamps (in seconds) indicating the start and end of the segment.
  - **text**: The transcribed text for that particular segment.
  - **tokens**: The token IDs processed by the model.
  - Additional metadata like `temperature`, `avg_logprob`, `compression_ratio`, and `no_speech_prob` that help evaluate the quality and confidence of the transcription.
- **language**: The detected or specified language of the audio.

The segmentation allows for precise alignment of text with the audio timeline, which is useful for subtitle generation, quality assessment, or further processing of specific parts of the transcription.

