
from app.schemas import PostCreate, ResponsePost, ResponseUser, UserCreated_and_Updated
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sql_app.database import  get_db
from sqlalchemy.orm import Session
from sql_app import models
from app.outh2 import get_current_user
from ..schemas import Vote

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/")
async def  votes_func(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
   #first we look for the vote if already exist 
   '''We make a query to see if Votes.posts.id == vote.post_id and Votes.users.id == current_user.id
   if found we raise  an exception cos we can not have more than one vote per user
   if not found we create a new vote'''
   vote_query = db.query(models.Votes).filter(models.Votes.posts_id == vote.posts_id, models.Votes.users_id == current_user.id)
   found_vote = vote_query.first()
   if vote.dir == 1:
       if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already voted")
       
       new_vote = models.Votes(posts_id = vote.posts_id, users_id = current_user.id)
       db.add(new_vote)
       db.commit()
       return {"message": "Successfully added vote"}
   else:
       if not found_vote:#if does not exist with raise an error cos there is nothing to delete
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
       
       vote_query.delete(synchronize_session=True)
       db.commit()
       return {"message": "Successfully deleted vote"}
    
       
     
     
    
      
