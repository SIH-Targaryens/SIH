from pydantic import BaseModel

class CollegeBase(BaseModel):
    college_name: str
    degree_course: str
    course_fees: str = None
    placements: str = None
    highest_package: str = None
    official_website: str = None
    city: str = None
    state: str = None

class CollegeOut(CollegeBase):
    id: int

    class Config:
        orm_mode = True