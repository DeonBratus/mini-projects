FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgresql://debral:12481632@localhost:5432/postgres 

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
