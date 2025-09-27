from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

from app.db import get_db
from app.models.college import College  
from app.models.commerce_college import CommerceCollege  

router = APIRouter()

class CollegeOut(BaseModel):
    college_name: str = Field(..., alias="College Name")
    degree_course: Optional[str] = Field(None, alias="Degree / Course")
    course_fees: Optional[str]
    placements: Optional[str]
    highest_package: Optional[str]
    official_website: Optional[str]
    city: Optional[str]
    state: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

@router.get("/compare_colleges", response_model=List[CollegeOut])
def compare_colleges(
    college_names: List[str] = Query(..., description="List of college names to compare"),
    stream: Literal["science", "commerce"] = Query(..., description="College stream"),
    db: Session = Depends(get_db)
):
    if stream == "science":
        colleges = db.query(College).filter(College.college_name.in_(college_names)).all()
    elif stream == "commerce":
        colleges = db.query(CommerceCollege).filter(CommerceCollege.college_name.in_(college_names)).all()
    else:
        raise HTTPException(status_code=400, detail="Invalid stream type")
    found_names = {getattr(c, "college_name") for c in colleges}
    missing = set(college_names) - found_names
    if missing:
        raise HTTPException(status_code=404, detail=f"Colleges not found: {', '.join(missing)}")
    return colleges
