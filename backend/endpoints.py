import os
import uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import UploadFile, File, Header, Depends, HTTPException
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
from datetime import date, timedelta
from typing import List


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

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)


from fastapi.middleware.cors import CORSMiddleware


app = fastapi.FastAPI()
logger.info("started")

# 1. Grab the origins from your .env file, default to localhost if not found
origins = os.getenv("ALLOWED_ORIGINS")

# 2. Apply the CORS rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploaded_images", exist_ok=True)

app.mount("/uploaded_images", StaticFiles(directory="uploaded_images"), name="images")

@app.post("/test")
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

@app.post("/create_user")
def create_user(data: schemas.UserCreate):
    session = Session()


    try:
        new_user = models.User(
            username=data.username,
            nickname=data.nickname, #type: ignore
            firstname=data.firstname,
            lastname=data.lastname,
            email=data.email,
            password=security.hash_password(data.password)
        )
        session.add(new_user)
        session.commit()

        token = security.create_token({"subject": data.username})
        logger.info(f"Successfully created user: {data.username}")
        return {"success": True, "message": f"User {data.username} created!", "token": token}

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
            
        if not security.verify_password(data.password, str(user.password)):
            logger.error(f"Failed to login user, invalid password: {data.password}")
            raise fastapi.HTTPException(status_code=401, detail="Invalid username or password")

        logger.info(f"Successfully login user: {data.username}")
        token = security.create_token({"subject": user.username})
        return {"success": True, "message": "Login successful!", "token": token, "firstname": user.firstname}
        
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
        if "." not in image_file.filename:
            logger.error(f"Failed to upload image: {image_file.filename} (No extension)")
            raise fastapi.HTTPException(status_code=400, detail="Invalid file. No extension found.")
            
        file_extension = image_file.filename.split(".")[-1].lower()

        allowed_extensions = ["jpg", "jpeg", "png", "heic"]

        if file_extension not in allowed_extensions:
            logger.error(f"Failed to upload image: {image_file.filename} (Invalid extension)")
            raise fastapi.HTTPException(status_code=400, detail="Invalid file. Only 'jpg jpeg png heic' images allowed.")

        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # The exact path on your hard drive
        file_path = f"uploaded_images/{unique_filename}"
        
        # Save the file to the hard drive
        with open(file_path, "wb") as buffer:
            buffer.write(await image_file.read())

        # Return the public URL to save in the database
        public_url = f"/uploaded_images/{unique_filename}"

        logger.info(f"Successfully uploaded image: {public_url}")
        return {"success": True, "image_url": public_url}
        
    except Exception as e:
        logger.error(f"Failed to upload image: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Failed to save image locally")


@app.get("/get_image")
def get_image(data: schemas.Image):
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
def create_plant(data: schemas.PlantCreate, user: str = Depends(security.get_user)):
    session = Session()
    try:

        new_plant = models.Plant(**data.model_dump())
        new_plant.username = user

        username = session.query(models.User).filter_by(username=user).first()

        if not username:
            raise fastapi.HTTPException(status_code=404, detail="User not found")

        today = date.today()
        if new_plant.water_frequency and not new_plant.date_next_water:
            new_plant.date_next_water = today + timedelta(days=new_plant.water_frequency)
        if new_plant.fertilizer_frequency and not new_plant.date_next_fertilized:
            new_plant.date_next_fertilized = today + timedelta(days=new_plant.fertilizer_frequency)
        if new_plant.pot_frequency and not new_plant.date_next_pot:
            new_plant.date_next_pot = today + timedelta(days=new_plant.pot_frequency)

        username.plants += 1
        session.add(new_plant)
        session.commit()
        
        session.refresh(new_plant)
        plant_id = new_plant.plant_id

        logger.info(f"Successfully created plant: {data.plant_name}")
        return {"success": True, "message": "Plant created!", "user": new_plant.username, "plant #": plant_id }

    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to create plant. Error: {e}")
        raise fastapi.HTTPException(status_code=400, detail=f"Failed to create plant. Error: {e}")

    finally:
        session.close()

@app.patch("/update_plant/{plant_id}")
def update_plant(data: schemas.PlantUpdate, plant_id: int, user: str = Depends(security.get_user)):
    session = Session()
    try:

        plant = session.get(models.Plant, plant_id)

        if not plant:
            fastapi.HTTPException(status_code=404, detail="Plant not found")
        if user != plant.username:
            raise fastapi.HTTPException(status_code=403, detail="no permission")

        today = date.today()
        if plant.water_frequency and not plant.date_next_water:
            plant.date_next_water = today + timedelta(days=plant.water_frequency)
        if plant.fertilizer_frequency and not plant.date_next_fertilized:
            plant.date_next_fertilized = today + timedelta(days=plant.fertilizer_frequency)
        if plant.pot_frequency and not plant.date_next_pot:
            plant.date_next_pot = today + timedelta(days=plant.pot_frequency)

        update = data.model_dump(exclude_unset=True)

        for item, value in update.items():
            setattr(plant, item, value)

        session.commit()
        session.refresh(plant)

        return {"success": True, "message": "Plant updated!"}

    except IntegrityError as e:

        session.rollback()
        logger.error(f"Failed to update plant. Error: {e}")
        raise fastapi.HTTPException(status_code=400, detail="Failed to update plant. Error: {e}")

    finally:
        session.close()

@app.patch("/update_user/")
def update_user(data: schemas.UserUpdate, username: str = Depends(security.get_user)):
    session = Session()
    try:
        user = session.query(models.User).filter_by(username=username).first()

        if not user:
            logger.info(f"Username not found: {username}")
            raise fastapi.HTTPException(status_code=404, detail="Username not found")
        if not security.verify_password(data.password, str(user.password)):
            logger.info(f"Password incorrect: {data.password}")
            raise fastapi.HTTPException(status_code=401, detail="Invalid password")

        new_data = data.model_dump(exclude_unset=True, exclude={'password'})

        for item, value in new_data.items():
            setattr(user, item, value)

        session.commit()
        
        # If the username was changed, we must issue a new token!
        new_token = None
        if data.username and data.username != username:
            new_token = security.create_token({"subject": data.username})

        return {"success": True, "message": "User settings updated!", "token": new_token}
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to update user. Error: {e}")
        raise fastapi.HTTPException(status_code=400, detail="Failed to update user. Error: {e}")
    finally:
        session.close()


@app.patch("/water_plant/{plant_id}")
def water_plants(plant_id: int, user: str = Depends(security.get_user)):
    session = Session()
    try:
        plant = session.query(models.Plant).filter_by(plant_id=plant_id, username=user).first()

        if not plant:
            raise fastapi.HTTPException(status_code=404, detail="Plant not found")

        today = date.today()
        plant.date_last_water = today
        plant.date_next_water = today + timedelta(days=plant.water_frequency)

        logger.info(f"Successfully watered plant: {plant_id}")
        session.commit()

        return {"success": True, "message": f"Plant watered! Next watering on {plant.date_next_water}"}

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching plant. Error: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Database error occurred")

    except IntegrityError as e:
        logger.error(f"Failed to fetch plant. Error: {e}")
        raise fastapi.HTTPException(status_code=404, detail="Plant not found")

    finally:
        session.close()

@app.patch("/fertilize_plant/{plant_id}")
def fertilize_plant(plant_id: int, user: str = Depends(security.get_user)):
    session = Session()
    try:
        plant = session.query(models.Plant).filter_by(plant_id=plant_id, username=user).first()

        if not plant:
            raise fastapi.HTTPException(status_code=404, detail="Plant not found")

        today = date.today()

        plant.date_last_fertilized = today
        plant.date_next_fertilized = today + timedelta(days=plant.fertilizer_frequency)
        logger.info(f"Successfully fertilized plant: {plant.plant_id}")
        session.commit()

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching plant. Error: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Database error occurred")

    except IntegrityError as e:
        logger.error(f"Failed to fetch plant. Error: {e}")
        raise fastapi.HTTPException(status_code=404, detail="Plant not found")

@app.patch("/pot_plant/{plant_id}")
def pot_plant(plant_id: int, user: str = Depends(security.get_user)):
    session = Session()
    try:
        plant = session.query(models.Plant).filter_by(plant_id=plant_id, username=user).first()
        if not plant:
            raise fastapi.HTTPException(status_code=404, detail="Plant not found")
        today = date.today()
        plant.date_last_pot = today
        plant.date_next_pot = today + timedelta(days=plant.pot_frequency)
        logger.info(f"repotted plant, next pot at: {plant.date_next_pot}")
        session.commit()

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching plant. Error: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Database error occurred")
    except IntegrityError as e:
        logger.error(f"Failed to fetch plant. Error: {e}")
        raise fastapi.HTTPException(status_code=404, detail="Plant not found")

@app.get("/all_plants/", response_model=list[schemas.PlantOut])
def all_plants(user: str = Depends(security.get_user)):
    session = Session()
    try:
        plants = session.query(models.Plant).filter_by(username=user).all()
        logger.info(f"Successfully fetched {len(plants)} plants")
        return plants
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching plants: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()


@app.get("/get_plant/{plant_id}", response_model=schemas.PlantOut)
def get_plant(plant_id: int, user: str = Depends(security.get_user)):
    session = Session()
    try:
        plant = session.query(models.Plant).filter_by(plant_id=plant_id, username=user).first()
        logger.info(f"Successfully fetched plant: {plant_id}")
        if not plant:
            raise fastapi.HTTPException(status_code=404, detail="Plant not found")
        return plant
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching plant. Error: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()

@app.get("/get_user")
def get_user(user: str = Depends(security.get_user)):
    session = Session()
    try:
        user = session.query(models.User).filter_by(username=user).first()
        logger.info(f"Successfully fetched user: {user.username}")
        if not user:
            raise fastapi.HTTPException(status_code=404, detail="No user found")
        
        user_data = {
            "username": user.username,
            "nickname": user.nickname,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email
        }
        return {"success": True, "user": user_data}

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching user. Error: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Database error occurred")
    finally:
        session.close()

# Serve the frontend at the root URL (Must be at the VERY BOTTOM or else the backend does load in time for the frontend!)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
