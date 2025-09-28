from pydantic import BaseModel

class CareerPathBase(BaseModel):
    career_role: str
    prerequisites: str = None
    average_salary: str = None
    key_recruiters: str = None
    mobility_stats: str = None
    next_steps: str = None

class CareerPathOut(CareerPathBase):
    id: int

    class Config:
        orm_mode = True