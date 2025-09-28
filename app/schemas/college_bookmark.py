from pydantic import BaseModel

class CollegeBookmarkBase(BaseModel):
    college_id: int
    college_type: str = "science"  # or "commerce"

class CollegeBookmarkCreate(CollegeBookmarkBase):
    pass

class CollegeBookmarkOut(CollegeBookmarkBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True