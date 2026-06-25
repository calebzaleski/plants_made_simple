import bcrypt

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
    
    # bcrypt checks if the new password hashes to the exact same result
    return bcrypt.checkpw(password_bytes, hashed_bytes)
