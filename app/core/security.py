from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from fastapi import HTTPException, status

password_hash = PasswordHash.recommended()

def hash_password(password:str) ->str:
    return password_hash.hash(password)

def verify_password(password:str, hashed_password:str)->bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(subject:str, role:str)->str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=60)
    payload= {
        "sub": subject,
        "role": role,
        "exp":expires_at
    }
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm= settings.ALGORITHM
    )
    return token

def decode_access_token(token:str)->dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
