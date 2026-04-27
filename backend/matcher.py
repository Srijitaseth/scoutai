import re
from embeddings import calculate_semantic_similarity


def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else "not_found@email.com"


def extract_name_from_resume(resume_text, filename):
    lines = resume_text.splitlines()

    blocked_words = [
        "education",
        "skills",
        "experience",
        "projects",
        "certifications",
        "achievements",
        "summary",
        "profile",
        "contact",
        "phone",
        "email",
        "linkedin",
        "github",
        "technical skills",
        "work experience",
        "professional experience"
    ]

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        if "@" in clean_line:
            continue

        if any(char.isdigit() for char in clean_line):
            continue

        if clean_line.lower() in blocked_words:
            continue

        words = clean_line.split()

        if len(words) >= 2 and len(words) <= 4:
            return clean_line.title()

    fallback_name = filename.replace(".pdf", "").replace("_", " ").replace("-", " ")
    return fallback_name.title()


def skill_score(required_skills, resume_text):
    if not required_skills:
        return 0, [], []

    matched = []
    missing = []

    for skill in required_skills:
        if skill.lower() in resume_text.lower():
            matched.append(skill)
        else:
            missing.append(skill)

    score = (len(matched) / len(required_skills)) * 100
    return round(score, 2), matched, missing


def calculate_rule_score(parsed_jd, resume_text):
    must_score, matched, missing = skill_score(
        parsed_jd["must_have_skills"],
        resume_text
    )

    nice_score, nice_matched, nice_missing = skill_score(
        parsed_jd["nice_to_have_skills"],
        resume_text
    )

    experience_score = 80
    domain_score = 75
    seniority_score = 80

    rule_score = (
        0.40 * must_score +
        0.25 * experience_score +
        0.15 * domain_score +
        0.10 * seniority_score +
        0.10 * nice_score
    )

    return round(rule_score, 2), matched, missing, nice_matched


def calculate_interest_score(resume_text):
    text = resume_text.lower()

    score = 65

    if "immediate" in text:
        score += 15

    if "30 days" in text:
        score += 10

    if "open to work" in text:
        score += 15

    if "actively looking" in text:
        score += 15

    return min(score, 100)


def match_candidate(jd_text, parsed_jd, resume_text, filename):
    semantic_score = calculate_semantic_similarity(jd_text, resume_text)

    rule_score, matched, missing, nice_matched = calculate_rule_score(
        parsed_jd,
        resume_text
    )

    match_score = round((0.60 * semantic_score) + (0.40 * rule_score), 2)

    interest_score = calculate_interest_score(resume_text)

    final_score = round((0.65 * match_score) + (0.35 * interest_score), 2)

    if final_score >= 85:
        action = "Schedule technical interview"
    elif final_score >= 70:
        action = "Recruiter review recommended"
    else:
        action = "Keep as backup or reject"

    return {
        "name": extract_name_from_resume(resume_text, filename),
        "email": extract_email(resume_text),
        "match_score": match_score,
        "interest_score": interest_score,
        "final_score": final_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "nice_to_have_matched": nice_matched,
        "recommended_action": action,
        "explanation": [
            f"Semantic similarity score is {semantic_score}",
            f"Rule-based score is {rule_score}",
            f"Matched skills: {', '.join(matched) if matched else 'None'}",
            f"Missing skills: {', '.join(missing) if missing else 'None'}"
        ]
    }