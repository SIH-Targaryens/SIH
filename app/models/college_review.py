from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class CollegeReview(Base):
    __tablename__ = "college_reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    college_id = Column(Integer, nullable=False)  
    college_type = Column(String, nullable=False)  
    rating = Column(Integer, nullable=False)  
    review_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
