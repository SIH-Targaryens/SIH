from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Literal
from app.db import get_db
from app.models.college import College
from app.models.commerce_college import CommerceCollege

router = APIRouter()

@router.get("/search_colleges")
def search_colleges(
    query: str = Query(..., description="College name or partial name"),
    stream: Literal["science", "commerce"] = Query(..., description="College stream"),
    db: Session = Depends(get_db)
):
    if stream == "science":
        colleges = db.query(College).filter(College.college_name.ilike(f"%{query}%")).all()
    elif stream == "commerce":
        colleges = db.query(CommerceCollege).filter(CommerceCollege.college_name.ilike(f"%{query}%")).all()
    else:
        return []
    return [
        {
            "College Name": c.college_name,
            "Degree / Course": getattr(c, "degree_course", None),
            "Course Fees": getattr(c, "course_fees", None),
            "Placements": getattr(c, "placements", None),
            "Highest Package": getattr(c, "highest_package", None),
            "Official Website": getattr(c, "official_website", None),
            "City": getattr(c, "city", None),
            "State": getattr(c, "state", None)
        }
        for c in colleges
    ]
