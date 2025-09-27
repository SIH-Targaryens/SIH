from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CommerceCollege(Base):
    __tablename__ = "commerce_colleges"  
    id = Column("S.no",Integer,  autoincrement=True)
    college_name = Column("College Name", String, primary_key=True, unique=True)
    degree_course = Column("Courses Offered", String)
    course_fees = Column("Average Fees(INR)", String)
    placements = Column("Average Placement (INR LPA)", Float)
    official_website = Column("Official Website", String)
    Location = Column("City/State", String)
    
    
