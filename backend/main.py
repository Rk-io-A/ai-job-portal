from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
import enum
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-in-production-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jobportal.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI(
    title="AI Job Portal API",
    description="Full Stack AI-Powered Job Portal Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELS ====================
class UserRole(str, enum.Enum):
    candidate = "candidate"
    employer = "employer"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(String, default=UserRole.candidate)
    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship("Job", back_populates="employer")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    location = Column(String)
    description = Column(Text)
    salary = Column(String, nullable=True)
    job_type = Column(String, default="Full-time")  # Full-time, Part-time, Remote
    employer_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    employer = relationship("User", back_populates="jobs")

Base.metadata.create_all(bind=engine)

# ==================== SCHEMAS ====================
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole = UserRole.candidate

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str
    salary: Optional[str] = None
    job_type: str = "Full-time"

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    salary: Optional[str]
    job_type: str
    created_at: datetime
    employer_id: int

    class Config:
        from_attributes = True

class AIMatchRequest(BaseModel):
    resume_text: str
    job_id: Optional[int] = None

# ==================== UTILS ====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# ==================== AUTH ROUTES ====================
@app.post("/auth/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        role=user.role.value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/auth/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# ==================== JOBS ROUTES ====================
@app.get("/jobs", response_model=List[JobOut])
def list_jobs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).offset(skip).limit(limit).all()
    return jobs

@app.post("/jobs", response_model=JobOut)
def create_job(job: JobCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.employer.value:
        raise HTTPException(status_code=403, detail="Only employers can post jobs")
    db_job = Job(**job.dict(), employer_id=current_user.id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# ==================== AI ROUTE (Mock for now) ====================
@app.post("/ai/match")
def ai_match(request: AIMatchRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Simple keyword-based matching for demo.
    Replace with OpenAI later for real AI matching.
    """
    jobs = db.query(Job).all()
    resume_lower = request.resume_text.lower()

    matches = []
    for job in jobs:
        score = 0
        title_words = job.title.lower().split()
        for word in title_words:
            if word in resume_lower:
                score += 20
        if job.location.lower() in resume_lower:
            score += 10
        if score > 0:
            matches.append({
                "job": {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location
                },
                "match_score": min(score, 100)
            })

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return {"matches": matches[:5], "message": "AI matching completed (keyword based demo)"}

@app.get("/")
def root():
    return {
        "message": "AI Job Portal API is running 🚀",
        "docs": "/docs",
        "author": "Rajiv Kapur"
    }
