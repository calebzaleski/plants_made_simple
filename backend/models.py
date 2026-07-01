import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Identity

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    # 'id' acts like SERIAL, but 'username' is your actual primary key based on your SQL
    id = Column(Integer, Identity(), unique=True)
    username = Column(String(20), primary_key=True, nullable=False)
    email = Column(String(80), nullable=False)
    nickname = Column(String(20))
    firstname = Column(String(40), nullable=False)
    lastname = Column(String(40), nullable=False)
    password = Column(String(255), nullable=False)
    plants = Column(Integer, nullable=False, default=0)
    joined = Column(Date, default=datetime.date.today())

    # This makes it easy in Python to get all plants owned by this user (e.g., my_user.user_plants)
    user_plants = relationship("Plant", back_populates="owner")

class Plant(Base):
    __tablename__ = 'plants'
    
    # plant_id SERIAL PRIMARY KEY
    plant_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign key linking back to the users table
    username: str = Column(String(20), ForeignKey('users.username', onupdate="CASCADE"), nullable=False)
    
    # Plant Details
    plant_name = Column(String(100), nullable=False)
    scientific_name = Column(String(150))
    age = Column(Integer)  # years
    image_url = Column(Text)
    health = Column(String(50))
    notes = Column(Text)
    
    # Care Needs
    light_needs = Column(String(255))
    fertilizer_needs = Column(String(255))
    
    # Dates
    date_acquired = Column(Date)
    date_last_water = Column(Date)
    date_next_water = Column(Date)
    water_frequency = Column(Integer) # days
    date_last_pot = Column(Date)
    pot_frequency = Column(Integer) # days
    date_next_pot = Column(Date)
    date_last_fertilized = Column(Date)
    fertilizer_frequency = Column(Integer) # days
    date_next_fertilized = Column(Date)

    # This links the relationship back to the User class
    owner = relationship("User", back_populates="user_plants")
