FROM python:3.12-slim
LABEL authors="calebzaleski"

WORKDIR /app

# Copy the files into a folder named 'backend' inside the container
COPY . ./backend

# Install the requirements from that new folder
RUN pip install -r backend/requirements.txt
RUN pip install --no-cache-dir "fastapi[standard]"

# Tell fastapi to run the file inside the backend folder
CMD ["fastapi", "dev", "backend/endpoints.py", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000