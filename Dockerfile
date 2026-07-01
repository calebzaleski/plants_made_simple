FROM python:3.12-slim
LABEL authors="calebzaleski"

WORKDIR /app

COPY backend/requirements.txt ./backend/
RUN pip install -r backend/requirements.txt
RUN pip install --no-cache-dir "fastapi[standard]"

COPY . .

CMD ["fastapi", "run", "backend/endpoints.py", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
