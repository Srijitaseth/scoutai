def safe_join(items):
    if not items:
        return "relevant skills"

    if isinstance(items, list):
        return ", ".join(str(item) for item in items[:6])

    return str(items)


def get_top_experience(parsed_resume):
    experience = parsed_resume.get("experience", [])

    if not experience:
        return ""

    first_exp = experience[0]

    if not isinstance(first_exp, dict):
        return str(first_exp)

    role = first_exp.get("role", "")
    company = first_exp.get("company", "")
    highlights = first_exp.get("highlights", [])

    highlight = ""
    if isinstance(highlights, list) and highlights:
        highlight = highlights[0]

    parts = [role, company, highlight]
    return " at ".join(part for part in [role, company] if part) + (
        f", where you {highlight}" if highlight else ""
    )


def get_top_project(parsed_resume):
    projects = parsed_resume.get("projects", [])

    if not projects:
        return ""

    first_project = projects[0]

    if not isinstance(first_project, dict):
        return str(first_project)

    name = first_project.get("name", "")
    technologies = safe_join(first_project.get("technologies", []))
    highlights = first_project.get("highlights", [])

    highlight = ""
    if isinstance(highlights, list) and highlights:
        highlight = highlights[0]

    if name and highlight:
        return f"your project {name}, where you {highlight}"

    if name:
        return f"your project {name} using {technologies}"

    return ""


def generate_outreach_email(candidate, parsed_jd):
    parsed_resume = candidate.get("parsed_resume", {})

    candidate_name = candidate.get("name", "there")
    job_title = parsed_jd.get("job_title", "this role")

    matched_skills = safe_join(candidate.get("matched_skills", []))
    missing_skills = candidate.get("missing_skills", [])

    responsibilities = parsed_jd.get("responsibilities", [])
    responsibility_text = safe_join(responsibilities[:3])

    top_experience = get_top_experience(parsed_resume)
    top_project = get_top_project(parsed_resume)

    personalization = ""

    if top_experience:
        personalization += f"I also noticed your experience as {top_experience}. "

    if top_project:
        personalization += f"Your work on {top_project} also stood out. "

    clarification_line = ""

    if missing_skills:
        clarification_line = (
            f"I would also like to briefly understand your exposure to "
            f"{safe_join(missing_skills[:2])}, as that appears to be an area for clarification."
        )

    email = f"""
Subject: {job_title} Opportunity Matching Your Background

Hi {candidate_name},

I came across your profile and noticed your experience with {matched_skills}. {personalization}

We are currently hiring for a {job_title} role. The role involves {responsibility_text}, which seems aligned with your background and project experience.

{clarification_line}

Would you be open to a quick conversation this week to explore this opportunity further?

Best regards,
Recruitment Team
"""

    return email.strip()