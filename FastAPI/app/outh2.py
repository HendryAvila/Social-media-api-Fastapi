from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.schemas import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sql_app.database import  get_db
from sqlalchemy.orm import Session
from sql_app.models import User
from app.config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# Provide:
'''
SECRET KEY
ALGORITHM
EXPIRATION TIME
'''
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_TIME = settings.expiration_time

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get("user_id"))
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

# This function takes the token from the request form automatically, extract the id for me, verify if the
# token is correct calling the function verify_access_token. We can pass this function as
# dependency in ours path operation to be secure

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        token = verify_access_token(token, credentials_exception)
        user = db.query(User).filter(User.id == token.id).first()
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error getting current user: {str(e)}",
                            headers={"WWW-Authenticate": "Bearer"})