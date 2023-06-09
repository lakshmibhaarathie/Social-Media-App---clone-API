# global modules
from fastapi import (Depends,status, APIRouter,HTTPException)
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func, case
from typing import List

# user-defined modules
from api import models
from api.schemas import (Post, UpdatePost, PostResponse, VoteRes)
from api.database import get_db
from api.routers import oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponse])
def get_posts(db:Session=Depends(get_db)
              , current_user=Depends(oauth2.get_current_user)):
    posts = db.query(models.Posts).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post:Post, db:Session=Depends(get_db)
                , current_user=Depends(oauth2.get_current_user)):
    """
    A pydantic model can be converted into a dictionary by adding .dict().
    """
    post_dict = post.dict()    # this going to convert our pydantic model to a dictionary
    post_dict.update({"user_id":current_user.id})

    """
    new_post = models.Posts(title=post.title, content=post.content
                            ,published=post.published)
    
    This can also be written as follows:
    """
    new_post = models.Posts(**post_dict)  # this creates the sql query to insert data

    db.add(new_post)    # here we perform the actual insertion of data
    db.commit()         # commit the changes to the database
    db.refresh(new_post)    # this act similar to RETURNING * statement from sql and fetch out query result

    return new_post
@router.get("/userposts",response_model=List[PostResponse])
def get_user_posts(db:Session=Depends(get_db)
                   , current_user=Depends(oauth2.get_current_user)):
    posts = db.query(models.Posts).filter(models.Posts.user_id==current_user.id).all()

    if not posts:
        return Response(content="No posts created by the user."
                        , status_code=status.HTTP_204_NO_CONTENT)
    return posts



@router.get("/{id}", response_model=PostResponse)
def get_post(id:int, db:Session=Depends(get_db)
             , current_user=Depends(oauth2.get_current_user)):

    post = db.query(models.Posts).filter(models.Posts.id==id).first()
    if not post:
        return Response(content=f"The requested post with id: {id} doesnot exists.",
                        status_code=status.HTTP_404_NOT_FOUND)
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    """
    The post to be deleted got checked for its existence with post_qry.
        Response is sent if the SQL couldn't find a post.
    On existence the post is deleted as followed.
    The changes are committed to db.
    """

    post_qry = db.query(models.Posts).filter(models.Posts.id==id)
    post = post_qry.first()
    if not post:
        return Response(content=f"There is no post with id: {id}.", status_code=status.HTTP_404_NOT_FOUND)
    if post.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied for the user to delete other user's post.")
    post_qry.delete(synchronize_session=False)  # as we are not expecting any output synchronize_session is set False
    db.commit()


@router.put("/{id}", response_model=PostResponse)
def update_post(id:int, post:UpdatePost, db:Session=Depends(get_db)
                , current_user=Depends(oauth2.get_current_user)):

    post_qry = db.query(models.Posts).filter(models.Posts.id==id)
    posts = post_qry.first()
    if not posts:
        return Response(content=f"The requested post with id: {id} doesnot exists."
                        , status_code=status.HTTP_404_NOT_FOUND)
    if posts.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied for the user to update other user's post.")
    post_qry.update(post.dict() , synchronize_session=False)      # type:ignore
    db.commit()

    return posts



@router.get("/votes/vote",response_model=List[VoteRes])
def get_post_votes(db:Session=Depends(get_db)
                   ,current_user=Depends(oauth2.get_current_user)):
    

    likes = func.sum(case(((models.Votes.vote == 1, 1)), else_=0)).label('likes') 
    dislikes = func.sum(case(((models.Votes.vote == -1, 1)), else_=0)).label('dislikes') 
   
    posts = db.query(models.Posts, likes, dislikes).join(
        models.Votes, models.Posts.id==models.Votes.post_id, isouter=True
        ).group_by(models.Posts.id).all()
    
    return posts