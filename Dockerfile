FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/tempFiles

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Run app when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
