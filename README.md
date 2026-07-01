# Plants Made Simple

Plants Made Simple is a lightweight, full-stack web application designed to take the guesswork out of plant care. It allows you to easily track watering schedules, manage fertilization, and save custom profiles with images for your entire plant collection.

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
      # IMPORTANT: Change ALLOWED_ORIGINS to match your server IP/domain
      - ALLOWED_ORIGINS=http://localhost:8000 
    depends_on:
      - db
    volumes:
      - ./uploaded_images:/app/uploaded_images

volumes:
  postgres_data:
  ```


2. Open your terminal in that folder and run:
```bash
docker-compose up -d
```
3. Access the application at `http://localhost:8000`
