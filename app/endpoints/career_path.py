from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app.models.career_path import CareerPath  

router = APIRouter()

def get_next_steps(node, db):
    
    if not node.next_steps:
        return []
    next_roles = [s.strip() for s in node.next_steps.split(";")]
  
    next_nodes = db.query(CareerPath).filter(CareerPath.career_role.in_(next_roles)).all()
    return [
        {
            "career role": n.career_role,
            "Category": n.prerequisites,
            "average_salary": n.average_salary,
            "Entrance Exams": [r.strip() for r in n.key_recruiters.split(",")] if n.key_recruiters else [],
            "SubCategory": n.mobility_stats,
        }
        for n in next_nodes
    ]

@router.get("/career_roadmap")
def career_roadmap(
    role: str = Query(..., description="Target career role (e.g., 'Chartered Accountant')"),
    db: Session = Depends(get_db)
):
    root = db.query(CareerPath).filter(CareerPath.career_role.ilike(role)).first()
    if not root:
        raise HTTPException(status_code=404, detail="Career role not found.")
    roadmap = {
        "career_role": root.career_role,
        "prerequisites": root.prerequisites,
        "average_salary": root.average_salary,
        "key_recruiters": [r.strip() for r in root.key_recruiters.split(",")] if root.key_recruiters else [],
        "mobility_stats": root.mobility_stats,
        "next_steps": get_next_steps(root, db)
    }
    return roadmap
