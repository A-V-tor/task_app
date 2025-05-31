FROM python:3.11-slim

WORKDIR /app

COPY . .
RUN pip install poetry && poetry install

EXPOSE 5000

CMD ["poetry", "run", "python", "main.py"]
