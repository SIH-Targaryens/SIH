from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.college_review import CollegeReview

router = APIRouter()

@router.post("/add_review")
def add_review(
    user_id: int = Query(...),
    college_id: int = Query(...),
    college_type: str = Query(...), 
    rating: int = Query(..., ge=1, le=5),
    review_text: str = Query(""),
    db: Session = Depends(get_db)
):
    
    existing = db.query(CollegeReview).filter_by(
        user_id=user_id, college_id=college_id, college_type=college_type
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="You already reviewed this college.")
    review = CollegeReview(
        user_id=user_id,
        college_id=college_id,
        college_type=college_type,
        rating=rating,
        review_text=review_text
    )
    db.add(review)
    db.commit()
    return {"status": "review added"}

@router.get("/college_reviews")
def get_reviews(
    college_id: int,
    college_type: str,
    db: Session = Depends(get_db)
):
    reviews = db.query(CollegeReview).filter_by(
        college_id=college_id, college_type=college_type
    ).all()
    return [
        {
            "user_id": r.user_id,
            "rating": r.rating,
            "review_text": r.review_text,
            "created_at": r.created_at
        }
        for r in reviews
    ]
