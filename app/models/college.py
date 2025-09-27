from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class College(Base):
    __tablename__ = "science colleges" 
    id = Column(Integer, autoincrement=True)
    college_name = Column("College Name", String, primary_key=True,unique=True)
    degree_course = Column("Degree / Course", String)
    course_fees = Column("Course Fees (approx, INR, 4-yr UG)", String)
    placements = Column("Placements (Avg package, LPA)", String)
    highest_package = Column("Highest package (LPA)", String)
    official_website = Column("Official Website", String)
