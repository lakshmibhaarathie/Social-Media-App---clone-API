from fastapi import APIRouter, HTTPException, status,Depends
from sqlalchemy.orm import Session

# user defined modules
from api import models, schemas
from api.routers import oauth2
from api.database import get_db

router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def voting(votes:schemas.Vote, db:Session=Depends(get_db)
           , current_user=Depends(oauth2.get_current_user)):
    
    post = db.query(models.Posts).filter(models.Posts.id==votes.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The requested post {votes.post_id} doesnot exists."
        )
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id==votes.post_id, models.Votes.user_id==current_user.id)
    
    found_vote = vote_query.first()
    
    if not found_vote:
        if votes.vote==0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"The user {current_user.id} have not voted yet."
            )
        new_vote = models.Votes(post_id=votes.post_id, user_id=current_user.id, vote=votes.vote)
        db.add(new_vote)
        db.commit()
        if votes.vote==1:
            return {"message":"The requested post liked successfully."}
        else:
            return {"message":"The requested post disliked successfully."}
    
        
    if votes.vote==0:
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"The voting status get deleted succesfully."}
    
    updated_vote = {
        "vote":votes.vote
    }
    
    vote_status = found_vote.vote

    if vote_status==1 and votes.vote==-1:
        vote_query.update(synchronize_session=False, values=updated_vote) # type:ignore
        db.commit()
        return {"message":"The requested post disliked succesfully."}
    elif vote_status==-1 and votes.vote==1:
        vote_query.update(synchronize_session=False, values=updated_vote) # type:ignore
        db.commit()
        return {"message":"The requested post liked succesfully."}
    else:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail=f"The user already have voted the same.")
    
    
