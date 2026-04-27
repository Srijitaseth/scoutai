import re


KNOWN_SKILLS = [
    "Python", "Java", "C#", ".NET", ".NET Core", "SQL", "React",
    "Node.js", "FastAPI", "Flask", "Django", "Machine Learning",
    "Deep Learning", "NLP", "AWS", "Azure", "Docker", "Kubernetes",
    "REST API", "Entity Framework", "MongoDB", "PostgreSQL"
]


def parse_jd(jd_text):
    found_skills = []

    for skill in KNOWN_SKILLS:
        if skill.lower() in jd_text.lower():
            found_skills.append(skill)

    experience_required = 0
    exp_match = re.search(r"(\d+)\+?\s*(years|yrs)", jd_text.lower())

    if exp_match:
        experience_required = int(exp_match.group(1))

    if "backend" in jd_text.lower():
        job_title = "Backend Developer"
    elif "data scientist" in jd_text.lower():
        job_title = "Data Scientist"
    elif "machine learning" in jd_text.lower():
        job_title = "Machine Learning Engineer"
    else:
        job_title = "Software Developer"

    return {
        "job_title": job_title,
        "must_have_skills": found_skills[:5],
        "nice_to_have_skills": found_skills[5:],
        "experience_required": experience_required,
        "seniority": "Mid-level" if experience_required >= 2 else "Entry-level",
        "location": "Not specified",
        "responsibilities": [
            "Build reliable software solutions",
            "Work with technical teams",
            "Deliver role-specific responsibilities"
        ],
        "disqualifiers": []
    }