FROM python:latest
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 1234
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "1234"]
