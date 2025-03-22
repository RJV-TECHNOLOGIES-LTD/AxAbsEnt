# AxAbsEnt Official Docker Runtime
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "umg/cycle2/scheduler.py"]