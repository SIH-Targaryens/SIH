from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Literal, Optional
from app.db import get_db
from app.models.college import College
from app.models.commerce_college import CommerceCollege
from app.models.career_path import CareerPath
from app.models.user_search_history import UserSearchHistory

router = APIRouter()

@router.get("/search")
def search_entities(
    query: str = Query(..., description="Name or partial name"),
    stream: Optional[Literal["science", "commerce", "career"]] = Query(None, description="Entity type to search"),
    user_id: int = Query(..., description="ID of the searching user"),
    db: Session = Depends(get_db)
):
    results = []
    search_type = stream or "college"

    
    db.add(UserSearchHistory(
        user_id=user_id,
        search_query=query,
        search_type=search_type
    ))
    db.commit()

    if stream == "science":
        results = db.query(College).filter(College.college_name.ilike(f"%{query}%")).all()
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
            for c in results
        ]
    elif stream == "commerce":
        results = db.query(CommerceCollege).filter(CommerceCollege.college_name.ilike(f"%{query}%")).all()
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
            for c in results
        ]
    elif stream == "career":
        results = db.query(CareerPath).filter(CareerPath.career_role.ilike(f"%{query}%")).all()
        return [
            {
                "Career Role": c.career_role,
                "Prerequisites": c.prerequisites,
                "Average Salary": c.average_salary,
                "Key Recruiters": c.key_recruiters,
                "Mobility Stats": c.mobility_stats,
                "Next Steps": c.next_steps
            }
            for c in results
        ]
    else:
        raise HTTPException(status_code=400, detail="Invalid stream/entity type specified.")
