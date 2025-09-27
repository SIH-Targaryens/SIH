from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CareerPath(Base):
    __tablename__ = "careermappingavgsalary"
    id = Column(Integer, autoincrement=True)
    career_role = Column("Career Role", String,  primary_key=True, unique=True, index=True, nullable=False)
    prerequisites = Column("Category", String) 
    average_salary = Column("Average Salary(INR/year)", String) 
    key_recruiters = Column("Entrance Exams", String)  
    mobility_stats = Column("Subcategory", String) 
