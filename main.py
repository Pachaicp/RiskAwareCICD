
from fastapi import FastAPI
from pydantic import BaseModel, Field
from database_validator import validate_database
from risk_engine import Release, analyze_release

app = FastAPI(
    title="Risk-Aware CI/CD Pipeline",
    description="API for evaluating software release risk",
    version="1.0.0",
)


class ReleaseRequest(BaseModel):
    code_change_size: int = Field(ge=0)
    tests_passed: bool
    database_breaking_change: bool
    previous_deployment_failed: bool
    security_check_passed: bool

class DatabaseValidationRequest(BaseModel):
    old_columns: list[str]
    new_columns: list[str]
    sql_script: str = "" 

@app.get("/")
def home():
    return {
        "project": "Risk-Aware CI/CD Pipeline",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze")
def analyze(request: ReleaseRequest):
    release = Release(**request.model_dump())
    return analyze_release(release)

@app.post("/database/validate")
def database_validate(request: DatabaseValidationRequest):
    return validate_database(
        old_columns=request.old_columns,
        new_columns=request.new_columns,
        sql_script=request.sql_script,
    )