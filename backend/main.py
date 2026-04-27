import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from database import create_tables
from resume_parser import extract_text_from_pdf
from jd_parser_ai import parse_jd_with_ai
from resume_parser_ai import parse_resume_with_ai
from matching_agent import match_structured_candidate
from outreach import generate_outreach_email
from feedback import save_feedback
from export_utils import export_csv, export_pdf
from dashboard import generate_dashboard_data
from conversation_agent import (
    start_agent_conversation,
    generate_next_agent_reply,
    score_interest_locally,
    MAX_CHAT_MESSAGES
)
from email_sender import send_outreach_email

DEFAULT_FRONTEND_URLS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def get_frontend_urls():
    frontend_urls = os.getenv("FRONTEND_URLS") or os.getenv("FRONTEND_URL")

    if not frontend_urls:
        return DEFAULT_FRONTEND_URLS

    parsed_urls = [
        url.strip().rstrip("/")
        for url in frontend_urls.split(",")
        if url.strip()
    ]

    return parsed_urls or DEFAULT_FRONTEND_URLS


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_frontend_urls(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()

UPLOAD_DIR = "uploads"
EXPORT_DIR = "exports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

latest_candidates = []
latest_parsed_jd = {}
latest_raw_jd = ""


@app.get("/")
def home():
    return {"message": "ScoutAI backend is running"}


@app.post("/parse-jd")
def parse_job_description(jd_text: str = Form(...)):
    global latest_parsed_jd, latest_raw_jd

    parsed = parse_jd_with_ai(jd_text)
    latest_parsed_jd = parsed
    latest_raw_jd = jd_text

    return {
        "raw_jd": jd_text,
        "parsed_jd": parsed
    }


@app.post("/upload-resumes")
def upload_resumes(jd_text: str = Form(...), files: list[UploadFile] = File(...)):
    global latest_candidates, latest_parsed_jd, latest_raw_jd

    latest_raw_jd = jd_text

    parsed_jd = parse_jd_with_ai(jd_text)
    latest_parsed_jd = parsed_jd

    results = []

    for index, file in enumerate(files, start=1):
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resume_text = extract_text_from_pdf(file_path)

        parsed_resume = parse_resume_with_ai(resume_text)

        candidate = match_structured_candidate(
            jd_text=jd_text,
            resume_text=resume_text,
            parsed_jd=parsed_jd,
            parsed_resume=parsed_resume
        )

        candidate["parsed_resume"] = parsed_resume
        candidate["id"] = index
        candidate["raw_resume_text"] = resume_text
        candidate["outreach_email"] = generate_outreach_email(candidate, parsed_jd)

        if "conversation" not in candidate:
            candidate["conversation"] = []

        candidate["conversation_completed"] = False
        candidate["interest_summary"] = candidate.get(
            "interest_summary",
            "Conversation not started yet"
        )

        results.append(candidate)

    results = sorted(results, key=lambda x: x["match_score"], reverse=True)

    for new_index, candidate in enumerate(results, start=1):
        candidate["id"] = new_index

    latest_candidates = results

    return {
        "parsed_jd": parsed_jd,
        "ranked_candidates": results
    }


@app.post("/start-conversation")
def start_conversation(candidate_id: int = Form(...)):
    global latest_candidates, latest_parsed_jd

    if candidate_id < 1 or candidate_id > len(latest_candidates):
        return {"error": "Invalid candidate ID"}

    candidate = latest_candidates[candidate_id - 1]

    first_message = start_agent_conversation(candidate, latest_parsed_jd)

    candidate["conversation"] = [first_message]
    candidate["conversation_completed"] = False
    candidate["interest_summary"] = "Conversation started"

    return {
        "candidate": candidate,
        "conversation": candidate["conversation"]
    }


@app.post("/candidate-reply")
def candidate_reply(candidate_id: int = Form(...), message: str = Form(...)):
    global latest_candidates, latest_parsed_jd

    if candidate_id < 1 or candidate_id > len(latest_candidates):
        return {"error": "Invalid candidate ID"}

    candidate = latest_candidates[candidate_id - 1]

    if "conversation" not in candidate or not candidate["conversation"]:
        first_message = start_agent_conversation(candidate, latest_parsed_jd)
        candidate["conversation"] = [first_message]

    if len(candidate["conversation"]) >= MAX_CHAT_MESSAGES:
        candidate["conversation_completed"] = True

        interest_result = score_interest_locally(candidate["conversation"])
        update_candidate_interest(candidate, interest_result)

        latest_candidates = sort_candidates_by_final_score(latest_candidates)

        return {
            "candidate": candidate,
            "conversation": candidate["conversation"],
            "interest_result": interest_result,
            "ranked_candidates": latest_candidates
        }

    candidate_message = {
        "speaker": "Candidate",
        "message": message
    }

    candidate["conversation"].append(candidate_message)

    if len(candidate["conversation"]) < MAX_CHAT_MESSAGES:
        try:
            agent_reply = generate_next_agent_reply(
                candidate=candidate,
                parsed_jd=latest_parsed_jd,
                conversation=candidate["conversation"]
            )

            if len(candidate["conversation"]) < MAX_CHAT_MESSAGES:
                candidate["conversation"].append(agent_reply)

        except Exception as error:
            print("AI agent reply failed. Using fallback message:", error)

            if len(candidate["conversation"]) < MAX_CHAT_MESSAGES:
                candidate["conversation"].append({
                    "speaker": "Agent",
                    "message": (
                        "Thank you. Could you also confirm your availability, "
                        "preferred work location, and expected compensation?"
                    )
                })

    if len(candidate["conversation"]) >= MAX_CHAT_MESSAGES:
        candidate["conversation"] = candidate["conversation"][:MAX_CHAT_MESSAGES]
        candidate["conversation_completed"] = True
    else:
        candidate["conversation_completed"] = False

    interest_result = score_interest_locally(candidate["conversation"])
    update_candidate_interest(candidate, interest_result)

    latest_candidates = sort_candidates_by_final_score(latest_candidates)

    return {
        "candidate": candidate,
        "conversation": candidate["conversation"],
        "interest_result": interest_result,
        "ranked_candidates": latest_candidates
    }


def update_candidate_interest(candidate, interest_result):
    candidate["interest_score"] = interest_result.get("interest_score", 0)
    candidate["interest_summary"] = interest_result.get("summary", "")
    candidate["interest_level"] = interest_result.get("interest_level", "")
    candidate["positive_signals"] = interest_result.get("positive_signals", [])
    candidate["concerns"] = interest_result.get("concerns", [])

    candidate["final_score"] = round(
        (0.65 * candidate["match_score"]) + (0.35 * candidate["interest_score"]),
        2
    )

    if candidate["final_score"] >= 85:
        candidate["recommended_action"] = "Schedule recruiter screening"
    elif candidate["final_score"] >= 70:
        candidate["recommended_action"] = "Recruiter review recommended"
    else:
        candidate["recommended_action"] = "Needs manual review"


def sort_candidates_by_final_score(candidates):
    sorted_candidates = sorted(
        candidates,
        key=lambda x: x["final_score"],
        reverse=True
    )

    for new_index, candidate in enumerate(sorted_candidates, start=1):
        candidate["id"] = new_index

    return sorted_candidates


@app.post("/feedback")
def add_feedback(candidate_id: int = Form(...), feedback_type: str = Form(...), comment: str = Form("")):
    global latest_candidates

    save_result = save_feedback(candidate_id, feedback_type, comment)

    if 0 <= candidate_id - 1 < len(latest_candidates):
        latest_candidates[candidate_id - 1]["recruiter_feedback"] = feedback_type

    return save_result


@app.post("/send-email")
def send_email(
    to_email: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...)
):
    return send_outreach_email(to_email, subject, body)


@app.get("/dashboard")
def dashboard():
    return generate_dashboard_data(latest_candidates)


@app.get("/export/csv")
def download_csv():
    file_path = os.path.join(EXPORT_DIR, "shortlist.csv")
    export_csv(latest_candidates, file_path)
    return FileResponse(file_path, filename="shortlist.csv")


@app.get("/export/pdf")
def download_pdf():
    file_path = os.path.join(EXPORT_DIR, "shortlist.pdf")
    export_pdf(latest_candidates, file_path)
    return FileResponse(file_path, filename="shortlist.pdf")
