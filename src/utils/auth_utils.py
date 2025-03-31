from fastapi import Depends, status
from passlib.context import CryptContext
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from jwt.exceptions import InvalidTokenError

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHAM = os.environ["ALGORITHAM"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id, role):
    try:
        jwt_encode = jwt.encode(payload={"sub" : user_id, "role": role},key=SECRET_KEY, algorithm=ALGORITHAM)
        return jwt_encode

    except Exception as e:
        raise Exception(f"error : {e}")

   
    
async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHAM])
        user_data = payload.get("sub")
        if user_data is None:
            raise credentials_exception
        
        return payload        
        
    except InvalidTokenError:
        raise credentials_exception

    