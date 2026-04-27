# ScoutAI - AI-Powered Talent Scouting and Engagement Agent

ScoutAI is an AI-powered talent scouting and candidate engagement platform designed to help recruiters move from a job description to an actionable ranked shortlist.

The system accepts a job description as input, parses role requirements, extracts structured information from uploaded resume PDFs, matches candidates using semantic and rule-based scoring, engages candidates through an AI-powered conversation interface, calculates interest signals, and exports a recruiter-ready shortlist.

## Problem Statement

Recruiters spend hours reviewing profiles and following up with candidates to understand whether they are both qualified and genuinely interested.

ScoutAI solves this by building an AI agent that:

- Takes a job description as input
- Discovers matching candidates from uploaded resume PDFs
- Parses resumes into structured candidate profiles
- Calculates a Match Score based on role fit
- Engages candidates conversationally through a candidate portal
- Calculates an Interest Score from candidate responses
- Outputs a ranked shortlist for recruiter action

## Features

### Recruiter Portal

The recruiter portal allows recruiters to:

- Paste a job description
- Upload candidate resume PDFs
- Parse the job description into structured role requirements
- Parse resumes into structured candidate profiles
- View ranked candidates
- View Match Score, Interest Score, and Final Score
- View matched skills and missing skills
- Review parsed resume details
- Generate customized outreach emails
- Send outreach emails to candidates
- Add recruiter feedback such as Shortlist, Reject, Good Match, or Not Relevant
- Export shortlisted candidates as CSV or PDF
- View dashboard charts and score summaries

### Candidate Portal

The candidate portal allows candidates to:

- Interact with the ScoutAI engagement agent
- Answer role-interest questions
- Confirm location flexibility, availability, compensation expectations, and skill confidence
- Complete a controlled conversation within a maximum of 10 chat messages
- Generate an Interest Score based on actual responses

### Export System

The export system generates recruiter-ready CSV and PDF reports including:

- Candidate rank
- Candidate name and email
- Match Score
- Interest Score
- Final Score
- Interest level
- Matched skills
- Missing skills
- Why the candidate matched
- Education summary
- Experience summary
- Project summary
- Conversation summary
- Positive interest signals
- Concerns
- Recruiter feedback
- Recommended action

## Tech Stack

### Frontend

- React
- Vite
- Recharts
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- PyMuPDF
- Sentence Transformers
- Scikit-learn
- ReportLab
- Gemini API
- SQLite

### AI Components

- Gemini API for job description parsing, resume parsing, and agent responses
- Sentence Transformer embeddings for semantic similarity
- Local rule-based scoring for Interest Score to reduce API usage and avoid quota issues

## Project Structure

```text
scoutai/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── jd_parser.py
│   ├── jd_parser_ai.py
│   ├── resume_parser.py
│   ├── resume_parser_ai.py
│   ├── matching_agent.py
│   ├── matcher.py
│   ├── embeddings.py
│   ├── outreach.py
│   ├── conversation_agent.py
│   ├── feedback.py
│   ├── export_utils.py
│   ├── dashboard.py
│   ├── email_sender.py
│   ├── uploads/
│   ├── exports/
│   ├── requirements.txt
│   └── scoutai.db
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── index.css
│   │   └── components/
│   │       ├── JDInput.jsx
│   │       ├── ResumeUpload.jsx
│   │       ├── CandidateTable.jsx
│   │       ├── CandidateDetails.jsx
│   │       ├── CandidatePortal.jsx
│   │       ├── RealAgentChat.jsx
│   │       ├── FeedbackButtons.jsx
│   │       ├── SendEmailButton.jsx
│   │       ├── DashboardCharts.jsx
│   │       └── ExportButtons.jsx
│
└── README.md