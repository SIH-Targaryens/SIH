from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from app.db import get_db
from app.models.user_search_history import UserSearchHistory
from app.models.college import College
from app.models.career_path import CareerPath

router = APIRouter()

@router.get("/recommendations")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    
    freq_searches = (
        db.query(
            UserSearchHistory.search_query,
            UserSearchHistory.search_type,
            func.count(UserSearchHistory.id).label("count")
        )
        .filter(UserSearchHistory.user_id == user_id)
        .group_by(UserSearchHistory.search_query, UserSearchHistory.search_type)
        .order_by(desc("count"))
        .limit(5)
        .all()
    )
    
    recommendations = []
    for search in freq_searches:
        if search.search_type == "college":
            rec = db.query(College).filter(College.college_name.ilike(f"%{search.search_query}%")).first()
            if rec:
                recommendations.append({
                    "type": "college",
                    "title": rec.college_name,
                    "details": {
                        "location": getattr(rec, "city", None),
                        "fees": getattr(rec, "course_fees", None),
                        "website": getattr(rec, "official_website", None)
                    }
                })
        elif search.search_type == "career":
            rec = db.query(CareerPath).filter(CareerPath.career_role.ilike(f"%{search.search_query}%")).first()
            if rec:
                recommendations.append({
                    "type": "career",
                    "title": rec.career_role,
                    "details": {
                        "salary": rec.average_salary,
                        "recruiters": rec.key_recruiters
                    }
                })
    return recommendations
