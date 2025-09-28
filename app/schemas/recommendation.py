from pydantic import BaseModel

class RecommendationOut(BaseModel):
    type: str  # "college" or "career"
    title: str
    details: dict