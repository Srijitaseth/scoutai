from llm_client import call_llm_json


def parse_resume_with_ai(resume_text):
    prompt = f"""
You are an expert resume parser.

Extract real structured candidate information from this resume text.

Return ONLY valid JSON. Do not use markdown.

JSON format:
{{
  "name": "",
  "email": "",
  "phone": "",
  "location": "",
  "summary": "",
  "education": [
    {{
      "degree": "",
      "institution": "",
      "duration": "",
      "score": ""
    }}
  ],
  "skills": {{
    "programming": [],
    "data_analytics": [],
    "cloud_security": [],
    "tools": [],
    "core_cs": [],
    "soft_skills": []
  }},
  "experience": [
    {{
      "company": "",
      "role": "",
      "location": "",
      "duration": "",
      "highlights": []
    }}
  ],
  "projects": [
    {{
      "name": "",
      "technologies": [],
      "duration": "",
      "highlights": []
    }}
  ],
  "certifications": [],
  "achievements": [],
  "total_experience": "",
  "notice_period": "",
  "expected_salary": "",
  "work_authorization": ""
}}

Resume Text:
{resume_text}
"""

    return call_llm_json(prompt)