# ScoutAI

ScoutAI is an AI-powered talent scouting and engagement agent. It helps recruiters parse job descriptions, analyze resume PDFs, calculate Match Score and Interest Score, engage candidates through an AI chat agent, collect recruiter feedback, and export a ranked shortlist as CSV or PDF.

## Features

- Job description parsing
- Resume PDF upload and parsing
- Semantic candidate matching
- Match Score, Interest Score, and Final Score
- Recruiter Portal and Candidate Portal
- AI candidate conversation
- Customized outreach email generation
- Recruiter feedback
- Dashboard charts
- CSV and PDF export

## Tech Stack

### Frontend

- React
- Vite
- Recharts

### Backend

- Python
- FastAPI
- SQLite
- PyMuPDF
- Sentence Transformers
- Gemini API
- ReportLab

## Project Structure

```text
scoutai/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── uploads/
│   └── exports/
│
├── frontend/
│   ├── package.json
│   └── src/
│
└── README.md
```

## How to Run

### 1. Start Backend

Open terminal 1:

```bash
cd /Users/srijitaseth/scoutai/scoutai/backend
source venv/bin/activate
```

Install dependencies if needed:

```bash
pip install -r requirements.txt
```

Set Gemini API environment variables:

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export GEMINI_MODEL="gemini-2.5-flash-lite"
```

Optional email setup:

```bash
export SCOUTAI_EMAIL="your_email@gmail.com"
export SCOUTAI_EMAIL_PASSWORD="your_gmail_app_password_here"
```

Optional frontend URL setup:

```bash
export FRONTEND_URL="http://localhost:5173"
```

Run backend:

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

### 2. Start Frontend

Open terminal 2:

```bash
cd /Users/srijitaseth/scoutai/scoutai/frontend
```

Install dependencies if needed:

```bash
npm install
```

Run frontend:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

Open the frontend URL in your browser.

## Usage

1. Open the Recruiter Portal.
2. Paste a job description.
3. Upload resume PDFs.
4. Click Analyze Candidates.
5. Review ranked candidates and scores.
6. Open Candidate Portal.
7. Start the AI agent conversation.
8. Enter candidate replies.
9. Return to Recruiter Portal.
10. Add recruiter feedback.
11. Export CSV or PDF shortlist.

## Notes

* Gemini API key is required for AI parsing and agent replies.
* If email sending is used, Gmail App Password is required.
* The backend reads allowed frontend origins from `FRONTEND_URL` or `FRONTEND_URLS`. Use `FRONTEND_URLS` as a comma-separated list if you need more than one origin.
* Do not commit API keys or passwords to GitHub.
* If Gemini quota is exceeded, wait and retry or use a fallback parser.

## Vercel Environment Variables

Set these in your Vercel project settings:

```text
FRONTEND_URL=https://your-frontend.vercel.app
```

If you deploy separate preview/production frontends, use:

```text
FRONTEND_URLS=https://your-production.vercel.app,https://your-preview.vercel.app
```

For the Vite frontend, set the backend URL:

```text
VITE_BACKEND_URL=https://your-backend-domain.example.com
```

## Sample Run Commands

### Backend

```bash
cd /Users/srijitaseth/scoutai/scoutai/backend
source venv/bin/activate
export GEMINI_API_KEY="your_gemini_api_key_here"
export GEMINI_MODEL="gemini-2.5-flash-lite"
uvicorn main:app --reload
```

### Frontend

```bash
cd /Users/srijitaseth/scoutai/scoutai/frontend
npm run dev
```
