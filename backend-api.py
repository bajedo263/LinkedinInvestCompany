from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import jwt
from datetime import datetime, timedelta
import numpy as np
from pydantic import BaseModel

app = FastAPI(title="Job Market Analysis API")

# Modèles Pydantic pour la validation des données
class JobOffer(BaseModel):
    id: Optional[int]
    company_id: int
    title: str
    description: str
    salary_min: Optional[float]
    salary_max: Optional[float]
    location: str
    domain: str
    skills: List[str]

class Company(BaseModel):
    id: Optional[int]
    name: str
    sector: str

class ApiKeyResponse(BaseModel):
    key: str
    expires_at: datetime

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de sécurité
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not is_valid_api_key(api_key):
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

# Routes API
@app.post("/api/keys/generate")
async def generate_api_key(admin_key: str):
    if admin_key != "ADMIN_SECRET_KEY":  # À remplacer par une vraie vérification
        raise HTTPException(status_code=403, detail="Invalid admin key")
    
    key = generate_unique_key()
    expires_at = datetime.utcnow() + timedelta(days=30)
    
    await store_api_key(key, expires_at)
    
    return ApiKeyResponse(key=key, expires_at=expires_at)

@app.get("/api/companies")
async def get_companies(api_key: str = Depends(verify_api_key)):
    companies = await get_companies_from_db()
    return companies

@app.get("/api/companies/{company_id}/jobs")
async def get_company_jobs(
    company_id: int,
    api_key: str = Depends(verify_api_key)
):
    jobs = await get_jobs_for_company(company_id)
    return jobs

@app.get("/api/companies/{company_id}/investment-analysis")
async def get_investment_analysis(
    company_id: int,
    api_key: str = Depends(verify_api_key)
):
    analysis = await analyze_company_investments(company_id)
    return analysis

@app.post("/api/crawler/trigger")
async def trigger_crawler(
    company_id: Optional[int] = None,
    api_key: str = Depends(verify_api_key)
):
    task_id = await schedule_crawler_task(company_id)
    return {"task_id": task_id}
