
from app.schemas import PostCreate, ResponsePost, ResponseUser, UserCreated_and_Updated
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sql_app.database import  get_db
from sqlalchemy.orm import Session
from sql_app import models
from app.outh2 import get_current_user
from typing import Optional

router = APIRouter(prefix="/posts", tags=["Posts"])

#-----------------------------------------------------------------------------------------------------------------
@router.get("/", response_model=list[ResponsePost])
async def get_posts(db: Session = Depends(get_db),
                    limit: int = 10,
                    skip: int = 0,
                    search: Optional[str] = ""):#query parameter
    # posts_db = cursor.execute("SELECT * FROM posts")
    # posts_db = cursor.fetchall()
    print(limit)
    posts_db = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    if not posts_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Couldn't be found the post")
    return posts_db

###Care full With Orders of requests###
@router.get("/{id}", response_model=ResponsePost)#path query
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):#request body
    # cursor.execute("SELECT * FROM posts WHERE id_post = %s", (str(id),))
    # post_db= cursor.fetchone()
                                  #filter is like the statement WHERE
    post_db = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Couldn't be found the post")

    return post_db
#------------------------------------------------------------------------------------------------------------------
#import logging
# logger.error(f"Error in create_post: {e}")
# logger = logging.getLogger(__name__)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
async def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        # cursor.execute(''' INSERT INTO posts (title, content, published)
        #           VALUES (%s, %s, %s) RETURNING * ''',
        #           (post.title, post.content, post.published))
        print(current_user.email)
        new_post = models.Post(owner_id=current_user.id,**post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)#this will be like tghe statement RETURNING
        return new_post
    except Exception as e:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Couldn't create the post. {e}")

#----------------------------------------------------------------------------------
@router.put("/{id}", response_model=ResponsePost)
async def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):#request body = post
    # cursor.execute("""UPDATE  posts SET title = %s, content = %s, published = %s where id_post = %s RETURNING *""",(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post_updated = updated_post.first()
    if post_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Couldn't be found the post")
      
    if post_updated.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")     
        
    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_updated
#------------------------------------------------------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id_post = %s", (str(id),))
    # conn.commit()
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post_deleted = deleted_post.first()
    if post_deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Couldn't be found the post")
        
    if post_deleted.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")    
        
    deleted_post.delete(synchronize_session=False)
    db.commit()   
    return Response(status_code=status.HTTP_204_NO_CONTENT)
