# AI Job Portal 🚀

**Full Stack Portfolio Project** — AI-Powered Job Board

A modern full-stack application where companies can post jobs and candidates get AI-powered job matching + resume analysis.

## 📁 Project Structure

```
ai-job-portal/
├── frontend/          # Next.js 14 + Tailwind CSS + TypeScript
├── backend/           # FastAPI + SQLAlchemy + PostgreSQL
├── .gitignore
└── README.md
```

## ✨ Features

- 🔐 JWT Authentication (Candidate & Employer roles)
- 📄 Job posting & searching
- 🤖 AI Resume Parser & Job Matching (OpenAI ready)
- 📊 Dashboard for Employers & Candidates
- 📱 Fully responsive UI
- ⚡ FastAPI backend with automatic docs (`/docs`)

## 🛠️ Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Frontend    | Next.js 14, TypeScript, Tailwind CSS, Shadcn/ui ready |
| Backend     | FastAPI, SQLAlchemy, Pydantic       |
| Database    | PostgreSQL (or SQLite for local)    |
| Auth        | JWT                                 |
| AI          | OpenAI API (optional)               |

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Rk-io-A/ai-job-portal.git
cd ai-job-portal
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 8000
```

Backend will run at: **http://localhost:8000**  
API Docs: **http://localhost:8000/docs**

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at: **http://localhost:3000**

## 🔑 Environment Variables

### Backend (`backend/.env`)
```env
DATABASE_URL=sqlite:///./jobportal.db
SECRET_KEY=your-super-secret-key-change-this
OPENAI_API_KEY=sk-xxxxxxxx   # optional
```

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📦 API Endpoints (Backend)

| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| POST   | `/auth/register`      | Register user              |
| POST   | `/auth/login`         | Login & get JWT            |
| GET    | `/jobs`               | List all jobs              |
| POST   | `/jobs`               | Create job (Employer)      |
| GET    | `/jobs/{id}`          | Get job details            |
| POST   | `/ai/match`           | AI job matching            |

## 👨‍💻 Author

**Rajiv Kapur**  
Software Architect & Full Stack Developer  
[Portfolio](https://rajivkapur.in.net) · [GitHub](https://github.com/Rk-io-A)

---

⭐ Star this repo if you find it useful!
