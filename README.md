# Plants Made Simple

Plants Made Simple is a lightweight, full-stack web application designed to take the guesswork out of plant care. It allows you to easily track watering schedules, manage fertilization, and save custom profiles with images for your entire plant collection.

<img width="1656" height="788" alt="Screenshot 2026-07-04 at 00 00 50" src="https://github.com/user-attachments/assets/e3e25427-1e3c-4154-9bcd-6aceab5f1ef5" />

## Dockercompose

```services:
  db:
    image: postgres:17-alpine
    container_name: postgres_server
    restart: unless-stopped
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: plants_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  server:
    image: ghcr.io/calebzaleski/plants_made_simple:latest
    container_name: fastapi-server
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - USER=admin
      - PASSWORD=mypassword
      - POSTGRES_DB=plants_db
      - DB_HOST=db
      - TZ=America/New_York
      - SECRET_KEY=your_super_secret_key_change_me
      - ALGORITHM=HS256
      - ALLOWED_ORIGINS=http://localhost:8000 
    depends_on:
      - db
    volumes:
      - ./uploaded_images:/app/uploaded_images

volumes:
  postgres_data:
  ```

1. update SECRET_KEY to anything over 32 characters. 

2. Open your terminal in that folder and run:
```bash
docker-compose up -d
```
3. Access the application at `http://localhost:8000`
