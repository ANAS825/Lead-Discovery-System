**Simple Lead Discovery System**

A backend system that allows users to add company information, automatically enrich it with decision-maker contact details using the Hunter.io API, and display results in a clean, searchable interface.
- This project was built as part of the ZiCloud Backend Intern Assignment and integrates with n8n for workflow automation.


**📌 Features**
- User Authentication — Simple login page with session management.
- Company Data Input — Add company name, website, and funding stage.
- Automated Lead Discovery — n8n workflow triggers Hunter.io API to fetch decision-maker contacts. 
- Data Storage — Company and contact details stored in a database.
- Results Display — View, search, and filter enriched contacts.
- Export to CSV .


**🛠️ Tech Stack**
- Backend: FastAPI (Python)
- Database: MySQL 
- Workflow Automation: n8n
- Lead Enrichment API: Hunter.io
- Frontend: HTML, CSS, JS


**⚙️ Installation & Setup**
- Clone The Repository (new version added)
- Create VE & install dependencies using requirement.txt
- Set Enviroment Variables (Hunter api & LLM model api Keys)
- run the backend server using cmd (uvicorn main:app --reload)
- **N8N Setup**:
    Create a new workflow using N8N
    Import the Lead Discovery System json file into your workflow
  




**🔚 API Endpoints**  
- "/" ---> for login page configuration and user authentication
- "/signup.html"  ---> for new user
- "/dashboard.html" ---> for dashboard page configuration
- "/results.html" ----> For result page configuration
- "/search" ---> Post enpoint for sending data into backend, database and trigger the N8N workflow
- "/N8N_Data" ---> Post endpoint for taking back emails and contacts from the N8N workflow into the backend
- "/chatbot" ---> Post endpoint for sending prompt to the chatbot


- GO TO "/docs" for documentations
  
  

