import os
import uuid
from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles
import fastapi
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from backend import schemas
from backend import models
from backend import security


#logger stuff
logger = logging.getLogger("proxy_server")
logging.basicConfig(filename='main.log', level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


#.env stuff
load_dotenv()
postgres_user = os.getenv("USER")
postgres_password = os.getenv("PASSWORD")
db = os.getenv("POSTGRES_DB")
port_env = os.getenv("INTERNAL_DB_PORT")
port = int(port_env) if port_env else None

#db connection stuff
my_url = URL.create(
    drivername="postgresql+psycopg",
    username=postgres_user,
    password=postgres_password,
    host = os.getenv("DB_HOST", "localhost"),
    port=port,
    database = db)
engine = create_engine(my_url)
Session = sessionmaker(bind=engine)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            logger.info("✅ SUCCESS: Connected to the database!")
            logger.info(f"Database Info: {result.scalar()}")
            return {"success": True, "Results": result}
    except Exception as e:
        logger.error("❌ FAILED to connect!")
        logger.error(f"Error details: {e}")
        return {"success": False, "Results": result}


app = fastapi.FastAPI()

os.makedirs("uploaded_images", exist_ok=True)

# 2. Tell FastAPI to serve this folder publicly at the /images URL
app.mount("/images", StaticFiles(directory="uploaded_images"), name="images")

@app.post("/test")
def test_app():
    test_connection()
    logger.info("/test command triggered")

@app.post("/create_user")
def create_user(data: schemas.UserCreate):
    session = Session()


    try:
        new_user = models.User(
            username=data.username,
            nickname=data.nickname,
            firstname=data.firstname,
            lastname=data.lastname,
            password=security.hash_password(data.password)
        )
        session.add(new_user)
        session.commit()
        
        logger.info(f"Successfully created user: {data.username}")
        return {"success": True, "message": f"User {data.username} created!"}
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to create user. prob the same username but = Error: {e}")
        raise fastapi.HTTPException(status_code=409, detail="User already exists! choose another name")

    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create user. Error: {e}")
        raise fastapi.HTTPException(status_code=400, detail="Username already exists or invalid data.")

    finally:
        session.close()

@app.post("/login_user")
def login_user(data: schemas.UserLogin):
    session = Session()
    try:
        # 1. Search the database for this username
        user = session.query(models.User).filter_by(username=data.username).first()
        
        # 2. If the user doesn't exist, fail
        if not user:
            logger.error(f"Failed to login user, invalid username: {data.username}")
            raise fastapi.HTTPException(status_code=401, detail="Invalid username")
            
        # 3. Check if the password matches the hashed password in the DB
        if not security.verify_password(data.password, user.password):
            logger.error(f"Failed to login user, invalid password: {data.password}")
            raise fastapi.HTTPException(status_code=401, detail="Invalid username or password")

        logger.info(f"Successfully login user: {data.username}")
        return {"success": True, "message": "Login successful!"}
        
    finally:
        session.close()

@app.post("/upload_image")
#needs to append the current plant model too
async def upload_image(image_file: UploadFile = File(...)):
    """
    Saves an uploaded image directly to the local hard drive 
    and returns the public URL.
    """
    try:
        # Give it a random unique name so images don't overwrite each other
        file_extension = image_file.filename.split(".")[-1].lower

        allowed_extensions = ["jpg", "jpeg", "png", "heic"]
        if file_extension not in allowed_extensions:
            raise fastapi.HTTPException(status_code=400, detail="Invalid file extension. Only images allowed.")

        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # The exact path on your hard drive
        file_path = f"uploaded_images/{unique_filename}"
        
        # Save the file to the hard drive
        with open(file_path, "wb") as buffer:
            buffer.write(await image_file.read())

        # Return the public URL to save in the database
        public_url = f"http://localhost:8000/images/{unique_filename}"

        logger.info(f"Successfully uploaded image: {public_url}")
        return {"success": True, "image_url": public_url}
        
    except Exception as e:
        logger.error(f"Failed to upload image: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Failed to save image locally")

@app.post("/get_image")
async def get_image(data: schemas.GetImg):
    session = Session()
    try:
        plant = session.query(models.Plant).filter_by(username=data.username, plant_id=data.plant_number).first()

        if plant:
            session.commit()
            logger.info(f"Successfully fetched image: {data.username}")
            return {"success": True, "image_url": plant.image_url}

        else:
            session.rollback()
            logger.error(f"Failed to fetch image: {data.username}")
            raise fastapi.HTTPException(status_code=404, detail="Plant not found")

    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to get image: {e}")
        raise fastapi.HTTPException(status_code=500,detail="Database error")

    finally:
        session.close()


@app.post("/create_plant")
async def create_plant(data: schemas.PlantCreate):
    session = Session()
    try:
        new_plant = models.Plant(**data.model_dump())
        session.add(new_plant)
        session.commit()
        
        session.refresh(new_plant)
        plant_id = new_plant.plant_id

        logger.info(f"Successfully created plant: {data.username}")
        return {"success": True, "message": "Plant created!", "user": data.username, "plant #": plant_id }
        
    finally:
        session.close()





