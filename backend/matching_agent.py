from embeddings import calculate_semantic_similarity


def flatten_skills(skills_dict):
    all_skills = []

    if isinstance(skills_dict, dict):
        for skill_list in skills_dict.values():
            if isinstance(skill_list, list):
                all_skills.extend(skill_list)

    elif isinstance(skills_dict, list):
        all_skills = skills_dict

    return all_skills


def calculate_skill_coverage(required_skills, candidate_skills):
    if not required_skills:
        return 0, [], []

    candidate_lower = [skill.lower() for skill in candidate_skills]

    matched = []
    missing = []

    for skill in required_skills:
        found = False

        for candidate_skill in candidate_lower:
            if skill.lower() in candidate_skill or candidate_skill in skill.lower():
                found = True
                break

        if found:
            matched.append(skill)
        else:
            missing.append(skill)

    score = (len(matched) / len(required_skills)) * 100
    return round(score, 2), matched, missing


def calculate_nice_to_have_score(nice_skills, candidate_skills):
    if not nice_skills:
        return 0, []

    candidate_lower = [skill.lower() for skill in candidate_skills]
    matched = []

    for skill in nice_skills:
        for candidate_skill in candidate_lower:
            if skill.lower() in candidate_skill or candidate_skill in skill.lower():
                matched.append(skill)
                break

    score = (len(matched) / len(nice_skills)) * 100
    return round(score, 2), matched


def match_structured_candidate(jd_text, resume_text, parsed_jd, parsed_resume):
    candidate_skills = flatten_skills(parsed_resume.get("skills", {}))

    must_have_skills = parsed_jd.get("must_have_skills", [])
    nice_to_have_skills = parsed_jd.get("nice_to_have_skills", [])

    must_score, matched_skills, missing_skills = calculate_skill_coverage(
        must_have_skills,
        candidate_skills
    )

    nice_score, nice_matched = calculate_nice_to_have_score(
        nice_to_have_skills,
        candidate_skills
    )

    semantic_score = calculate_semantic_similarity(jd_text, resume_text)

    experience_score = 80
    education_score = 80
    seniority_score = 80

    match_score = (
        0.35 * must_score +
        0.20 * semantic_score +
        0.15 * experience_score +
        0.10 * education_score +
        0.10 * seniority_score +
        0.10 * nice_score
    )

    match_score = round(match_score, 2)

    interest_score = 0
    final_score = round((0.65 * match_score) + (0.35 * interest_score), 2)

    if match_score >= 85:
        action = "Strong fit - start agent conversation"
    elif match_score >= 70:
        action = "Good fit - recruiter review recommended"
    else:
        action = "Needs manual review"

    return {
        "name": parsed_resume.get("name", "Unknown Candidate"),
        "email": parsed_resume.get("email", "not_found@email.com"),
        "phone": parsed_resume.get("phone", ""),
        "parsed_resume": parsed_resume,
        "match_score": match_score,
        "interest_score": interest_score,
        "final_score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "nice_to_have_matched": nice_matched,
        "recommended_action": action,
        "recruiter_feedback": "Not reviewed",
        "conversation": [],
        "interest_summary": "Conversation not started yet",
        "explanation": [
            f"Semantic similarity score: {semantic_score}",
            f"Must-have skill coverage score: {must_score}",
            f"Nice-to-have skill score: {nice_score}",
            f"Matched skills: {', '.join(matched_skills) if matched_skills else 'None'}",
            f"Missing skills: {', '.join(missing_skills) if missing_skills else 'None'}"
        ]
    }