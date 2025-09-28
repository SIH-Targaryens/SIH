from pydantic import BaseModel

class CollegeReviewBase(BaseModel):
    college_id: int
    college_type: str
    rating: int
    review_text: str = ""

class CollegeReviewCreate(CollegeReviewBase):
    pass

class CollegeReviewOut(CollegeReviewBase):
    id: int
    user_id: int
    created_at: str

    class Config:
        orm_mode = True