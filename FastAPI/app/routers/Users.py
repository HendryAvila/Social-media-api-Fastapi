
from app.schemas import PostCreate, ResponsePost, ResponseUser, UserCreated_and_Updated
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sql_app.database import  get_db
from sqlalchemy.orm import Session
from sql_app import models
from passlib.context import CryptContext


router = APIRouter(prefix="/users", tags=["users"])






#Hashing password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#----------------------USER PATH OPERATION---------------------------------------------------------
@router.get("/", response_model=list[ResponseUser])
async def get_users(db: Session = Depends(get_db)):
    users_db = db.query(models.User).all()
    if not users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is not users in your datab base")
    return users_db

@router.get("/{id}", response_model=ResponseUser)
async def get_user(id: int, db: Session = Depends(get_db)):
    user_db= db.query(models.User).filter(models.User.id == id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Couldn't be found the user")
    return user_db
    

#------------------------POST-------------------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
async def create_user(user: UserCreated_and_Updated, db: Session = Depends(get_db)):
        
        
        #hashing the user.password with the hash method
        hashed_password = pwd_context.hash(user.password)
        user.password = hashed_password
        
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        if not new_user:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Couldn't create the user")
        return new_user
            
        