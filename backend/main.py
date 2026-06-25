import os
import uuid
import shutil
from urllib import request

from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles
import fastapi
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pydantic import BaseModel
from backend import models
from backend import security


load_dotenv()

logger = logging.getLogger("proxy_server")

logging.basicConfig(filename='main.log', level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

user = os.getenv("USER")
password = os.getenv("PASSWORD")
db = os.getenv("POSTGRES_DB")
port = os.getenv("DB_PORT")

my_url = URL.create(
    drivername="postgresql+psycopg",
    username=user,
    password=password,
    host = os.getenv("DB_HOST", "localhost"),
    port=port,
    database = db
)
engine = create_engine(my_url)
Session = sessionmaker(bind=engine)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            logger.info("✅ SUCCESS: Connected to the database!")
            logger.info(f"Database Info: {result.scalar()}")
    except Exception as e:
        logger.error("❌ FAILED to connect!")
        logger.error(f"Error details: {e}")

# Run the test when this file is loaded

app = fastapi.FastAPI()

# 1. Create the folder if it doesn't exist yet
os.makedirs("uploaded_images", exist_ok=True)

# 2. Tell FastAPI to serve this folder publicly at the /images URL
app.mount("/images", StaticFiles(directory="uploaded_images"), name="images")

@app.post("/test")
def test_app():
    test_connection()
    logger.info("/test command triggered")
class UserCreate(BaseModel):
    username: str
    nickname: str
    firstname: str
    lastname: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


@app.post("/create_user")
def create_user(user_data: UserCreate):
    session = Session()


    try:
        new_user = models.User(
            username=user_data.username,
            nickname=user_data.nickname,
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            password=security.hash_password(user_data.password)
        )
        session.add(new_user)
        session.commit()
        
        logger.info(f"Successfully created user: {user_data.username}")
        return {"success": True, "message": f"User {user_data.username} created!"}
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
def login_user(login_data: UserLogin):
    session = Session()
    try:
        # 1. Search the database for this username
        user = session.query(models.User).filter_by(username=login_data.username).first()
        
        # 2. If the user doesn't exist, fail
        if not user:
            logger.error(f"Failed to login user, invalid username: {login_data.username}")
            raise fastapi.HTTPException(status_code=401, detail="Invalid username")
            
        # 3. Check if the password matches the hashed password in the DB
        if not security.verify_password(login_data.password, user.password):
            logger.error(f"Failed to login user, invalid password: {login_data.password}")
            raise fastapi.HTTPException(status_code=401, detail="Invalid username or password")

        logger.info(f"Successfully login user: {login_data.username}")
        return {"success": True, "message": "Login successful!"}
        
    finally:
        session.close()

@app.post("/upload_image")
async def upload_image(image_file: UploadFile = File(...)):
    """
    Saves an uploaded image directly to the local hard drive 
    and returns the public URL.
    """
    try:
        # Give it a random unique name so images don't overwrite each other
        file_extension = image_file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # The exact path on your hard drive
        file_path = f"uploaded_images/{unique_filename}"
        
        # Save the file to the hard drive
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
            
        # Return the public URL to save in the database
        public_url = f"http://localhost:8000/images/{unique_filename}"

        logger.info(f"Successfully uploaded image: {public_url}")
        return {"success": True, "image_url": public_url}
        
    except Exception as e:
        logger.error(f"Failed to upload image: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Failed to save image locally")








