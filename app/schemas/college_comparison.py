from pydantic import BaseModel
from typing import List

class CollegeComparisonRequest(BaseModel):
    college_ids: List[int]
    college_type: str  # "science" or "commerce"

class CollegeComparisonOut(BaseModel):
    colleges: List[dict]