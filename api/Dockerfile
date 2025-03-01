FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls -la

RUN echo '#!/bin/bash\necho "Current directory:"\npwd\necho "Directory contents:"\nls -la\necho "Python path:"\npython -c "import sys; print(sys.path)"\necho "Starting server..."\npython -c "import uvicorn; uvicorn.run(\"main:app\", host=\"0.0.0.0\", port=8000)"' > /app/start.sh \
    && chmod +x /app/start.sh

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["/app/start.sh"]
# CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]