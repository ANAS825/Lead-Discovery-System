import requests
from fastapi import FastAPI, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, Optional, List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
import os
from fastapi.encoders import jsonable_encoder
from openai import OpenAI


app = FastAPI()
load_dotenv()



# LLM API-Key Configuration (MODEL Used: Deepseek V3 model)
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= os.getenv("LLM_API_KEY"),

)

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)] 

BASE_DIR = Path(__file__).resolve().parent.parent  # go up from backend/ to project/


# chat model pydantic model
class Prompt(BaseModel):
    prompt: str



# Company_INFO pydantic model
class Company_INFO(BaseModel):
    Company_Name: str
    Website: str
    Funding_Stage: str

# Contacts Pydantic Model
class Contacts(BaseModel):
    Company_Name: str
    Name:str
    Email:str
    Title:Optional[str] 
    Executive: Optional[str]
    Department:Optional[str]
    Linkedin_url:Optional[str]
    Phone_Number: Optional[str]



# Trigger Workflow
def get_request( company:dict):
    r = requests.get(f"http://localhost:5678/webhook-test/f8e3f391-7cf1-470e-8f7a-d8851583f79b/company-search/{company.Company_Name}/{company.Website}/{company.Funding_Stage}")
    return( r.json())



# this endpoint will add the details from the form to database and trigger the workflow if it is a new company . if not it will search in cache system the retreive contacts
@app.post("/search")
async def search_company(request: Company_INFO, db: db_dependency):
        company_name = request.Company_Name.strip().upper()
        website = request.Website.strip()
        funding_stage = request.Funding_Stage.strip().title()

        db_company = models.Company_Info(
        Company_Name=company_name,
        Website=website,
        Funding_Stage=funding_stage)

        existing_company = db.query(models.Company_Info).filter(models.Company_Info.Company_Name == db_company.Company_Name).first()
        if  existing_company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        db.add(db_company)
        db.commit()
        get_request(db_company)
        if get_request:    
            return {"message": "Data sent to websocket successfully!"}
        

        return {"message": "Company added successfully!"}


# login page configuration with backend
@app.get("/",response_class=HTMLResponse)
def login():
    file_path = BASE_DIR / "frontend" / "login.html"
    if not file_path:
        return HTMLResponse(content="<h1>login.html not found</h1>", status_code=404)
    return file_path.read_text(encoding="utf-8") 

# dashboard  page Configuration with backend
@app.get("/dashboard.html", response_class=HTMLResponse)
def get_dashboard():
    file_path = BASE_DIR / "frontend" / "dashboard.html"
    if not file_path.exists():
        return HTMLResponse(content="<h1>dashboard.html not found</h1>", status_code=404)
    return file_path.read_text(encoding="utf-8")

# results page Configuration with backend
@app.get("/results.html", response_class=HTMLResponse)
def get_results():
    file_path = BASE_DIR / "frontend" / "results.html"
    if not file_path.exists():
        return HTMLResponse(content="<h1>results.html not found</h1>", status_code=404)
    return file_path.read_text(encoding="utf-8")



# Wrapper model for incoming payload
class ContactWrapper(BaseModel):
    data: List[Contacts]

# This endpoint is used to receive data from the N8N workflow created and save the data into a database
@app.post("/N8N_Data")
async def import_contacts(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    contacts = body.get("request", [])
    if not isinstance(contacts, list):
        return {"status": "error", "message": "Invalid format"}

    records_added = 0
    for contact in contacts:
        db_contact = models.Contacts(
            Company_Name=contact.get("Company_Name"),
            Name=contact.get("Name"),
            Email=contact.get("Email"),
            Title=contact.get("Title"),
            Executive=contact.get("Executive"),
            Department=contact.get("Department"),
            Linkedin_url=contact.get("Linkedin_url"),
            Phone_Number=contact.get("Phone_Number"),
        )
        x_contacts = db.query(models.Company_Info).filter(models.Company_Info == db_contact.Company_Name).first()
        if x_contacts:
            db_contact.Company_Name = x_contacts.Company_Name


        db.add(db_contact)
        records_added += 1

    db.commit()
    return {"status": "success", "records_added": records_added}

# this end point will fetch contacts details associated with the company
@app.get("/Fetch_Contacts")
async def from_db(company_name:str, db:db_dependency):
    request = db.query(models.Contacts).filter(models.Contacts.Company_Name == company_name.upper()).all()
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts Not Found!")
    return jsonable_encoder(request)


@app.post("/chatbot")
async def chatbot(request: Prompt):
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {
                "role": "system",
                "content": """"You are an expert email marketer. 
                            Given a contact's name and title, generate exactly ONE simple, 
                            personalized, and engaging email subject line. 
                            Keep it brief (under 10 words), professional, and relevant to their role. 
                            Return ONLY the subject line — no explanations, no parentheses, no extra text."""
            },
            {"role": "user", "content": request.prompt}
        ]
    )
    return {"response": response.choices[0].message.content.strip()}



