from llm_client import call_llm_json


def parse_jd_with_ai(jd_text):
    prompt = f"""
You are an expert technical recruiter.

Extract real structured hiring information from this job description.

Return ONLY valid JSON. Do not use markdown.

JSON format:
{{
  "job_title": "",
  "company_overview": "",
  "must_have_skills": [],
  "nice_to_have_skills": [],
  "responsibilities": [],
  "experience_required": "",
  "education": "",
  "location": "",
  "work_mode": "",
  "seniority": "",
  "domain": "",
  "compensation": "",
  "disqualifiers": []
}}

Job Description:
{jd_text}
"""

    return call_llm_json(prompt)