from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.college_bookmark import CollegeBookmark
from app.models.college import College  

router = APIRouter()

@router.post("/bookmark_college")
def bookmark_college(
    user_id: int = Query(...),
    college_id: int = Query(...),
    db: Session = Depends(get_db)
):
    
    college = db.query(College).filter(College.id == college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found.")
  
    existing = db.query(CollegeBookmark).filter_by(user_id=user_id, college_id=college_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Already bookmarked.")
    bookmark = CollegeBookmark(user_id=user_id, college_id=college_id)
    db.add(bookmark)
    db.commit()
    return {"status": "bookmarked"}

@router.delete("/bookmark_college")
def remove_bookmark(
    user_id: int = Query(...),
    college_id: int = Query(...),
    db: Session = Depends(get_db)
):
    bookmark = db.query(CollegeBookmark).filter_by(user_id=user_id, college_id=college_id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found.")
    db.delete(bookmark)
    db.commit()
    return {"status": "removed"}
