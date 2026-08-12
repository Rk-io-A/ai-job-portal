# AI Job Portal

Full-stack portfolio project demonstrating a job board with candidate/employer roles and optional AI-assisted matching.

> **Status:** engineering demo. Jobs, employers, candidates, resume scores and AI output in a demo environment are illustrative unless explicitly connected to real verified data.

## Stack

```text
Frontend   Next.js 14 + TypeScript + Tailwind CSS
Backend    FastAPI + SQLAlchemy + Pydantic
Database   SQLite locally / PostgreSQL-ready
Auth       JWT
AI         Optional provider integration
```

## Features

- candidate and employer account flows;
- job posting and search;
- dashboard patterns;
- resume-analysis / matching integration points;
- responsive UI;
- FastAPI documentation in local development.

## Local setup

Backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Environment

Backend example:

```env
DATABASE_URL=sqlite:///./jobportal.db
SECRET_KEY=REPLACE_WITH_A_RANDOM_SECRET
OPENAI_API_KEY=
```

Frontend:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Provider API keys and JWT signing secrets belong only on the backend.

## Security / production notes

Before any real hiring use, add verified employer authorization, object ownership, resume/file privacy controls, retention/deletion rules, rate limits, audit logs and appropriate AI transparency. Do not make automated employment decisions solely from an unvalidated demo score.

## Author

Rajiv Kapur — Software Architect & Full-Stack Developer

Portfolio: `https://rajivkapur.in.net`
