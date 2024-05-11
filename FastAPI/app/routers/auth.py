from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sql_app.database import get_db
from sql_app.models import User
from app.schemas import UserLogin
from passlib.context import CryptContext
from app.outh2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schemas import Token


router = APIRouter(tags=["authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post("/login", response_model=Token)
async def login(user_login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #OAuth2PasswordRequestForm is like the schema, it will take the username and password(username can be an email)
    #so it works for us and is more secure
    user = db.query(User).filter(User.email == user_login.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not pwd_context.verify(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    #create a token
    access_token = create_access_token(data={"user_id": user.id})
    
    #return the token
    return {"access_token": access_token, "token_type": "bearer"}


    