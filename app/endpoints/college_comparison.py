from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from app.db import get_db
from app.models.college import College  

router = APIRouter()


class CollegeOut(BaseModel):
    college_name: str = Field(..., alias="College Name")
    degree_course: Optional[str] = Field(None, alias="Degree / Course")
    course_fees: Optional[str] = Field(None, alias="Course Fees (approx, INR, 4-yr UG)")
    placements: Optional[str] = Field(None, alias="Placements (Avg package, LPA)")
    highest_package: Optional[str] = Field(None, alias="Highest package (LPA)")
    official_website: Optional[str] = Field(None, alias="Official Website")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True  

@router.get("/compare_colleges", response_model=List[CollegeOut])
def compare_colleges(
    college_names: List[str] = Query(..., description="List of college names to compare"),
    db: Session = Depends(get_db)
):
    
    colleges = db.query(College).filter(College.college_name.in_(college_names)).all()
    found_names = {getattr(c, "college_name") for c in colleges}
    missing = set(college_names) - found_names
    if missing:
        raise HTTPException(status_code=404, detail=f"Colleges not found: {', '.join(missing)}")
    return colleges
