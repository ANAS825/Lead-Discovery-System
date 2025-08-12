from sqlalchemy import  String, Integer, Column, ForeignKey
from database import Base
from database import engine




class Company_Info(Base):
    __tablename__ = "Company_info"

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Company_Name = Column(String(100), unique=True)
    Website = Column(String(200))
    Funding_Stage = Column(String(50))



class Contacts(Base):
    __tablename__ = "Contacts"

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Company_Name = Column(String(100), ForeignKey("Company_info.Company_Name"), nullable=False)
    Name = Column(String(100))
    Email = Column(String(100))
    Title = Column(String(100))
    Executive = Column(String(50))
    Department = Column(String(50))
    Linkedin_url = Column(String(200))
    Phone_Number = Column(String(20))


