# global-modules
from fastapi import (FastAPI, Depends,status)
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List


# user-defined modules
from api import models
from api.utils import pwd_encrypt
from api.schemas import (Post, UpdatePost, PostResponse, User, UserResponse)
from api.database import (get_db, engine)

# to create the table if not exists
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#                   **************************************    Posts  ********************************************

@app.get("/posts", response_model=List[PostResponse])
def get_posts(db:Session=Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post:Post, db:Session=Depends(get_db)):
    """
    A pydantic model can be converted into a dictionary by adding .dict().
    """

    post_dict = post.dict()    # this going to convert our pydantic model to a dictionary

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



@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id:int, db:Session=Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id==id).first()
    if not post:
        return Response(content=f"The requested post with id: {id} doesnot exists.",
                        status_code=status.HTTP_404_NOT_FOUND)
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db)):
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
    post_qry.delete(synchronize_session=False)  # as we are not expecting any output synchronize_session is set False
    db.commit()


@app.put("/posts/{id}", response_model=PostResponse)
def update_post(id:int, post:UpdatePost, db:Session=Depends(get_db)):
    post_qry = db.query(models.Posts).filter(models.Posts.id==id)
    posts = post_qry.first()
    if not posts:
        return Response(content=f"The requested post with id: {id} doesnot exists."
                        , status_code=status.HTTP_404_NOT_FOUND)
    
    post_qry.update(post.dict() , synchronize_session=False)
    db.commit()

    return posts



#                       **************************************    Users    ********************************************



@app.get("/users/{id}", response_model=UserResponse)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id==id).first()
    return user

@app.post("/users",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user:User, db:Session=Depends(get_db)):

    user.password = pwd_encrypt(user.password)
    user_dict = user.dict()
    new_user = models.Users(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)

    return new_user

