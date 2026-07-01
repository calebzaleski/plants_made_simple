from typing import Any
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from fastapi import Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

bearer_scheme = HTTPBearer()


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def hash_password(plain_text_password: str) -> str:
    """
    Takes a plain text password and returns a secure, irreversible hash string 
    ready to be saved in the database.
    """
    # Convert the string to bytes, then blend it!
    password_bytes = plain_text_password.encode('utf-8')
    
    # 'gensalt' adds random extra characters to make it even harder to crack
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    
    # Return it as a normal string so you can save it to your database
    return hashed_bytes.decode('utf-8')

def verify_password(plain_text_password: str, hashed_password_from_db: str) -> bool:
    """
    Checks if a plain text password matches a hash from the database.
    Returns True if correct, False if incorrect.
    """
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password_from_db.encode('utf-8')
    
    # bcrypt checks if the new password hashes to the exact
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"Error": "The token has expired."}
    except jwt.InvalidTokenError:
        return {"Error": "Invalid token signature or format."}


def get_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> Any | None:
    """
    FastAPI Dependency: Extracts the token from the header, verifies it, 
    and returns the username so it can be injected into secure routes.
    """
    token = credentials.credentials
    result = verify_token(token)
    
    if "Error" in result:
        raise HTTPException(status_code=401, detail=result["Error"])
        
    # Grab whichever key you ended up using (subject or sub)
    return result.get("subject", result.get("subject"))


