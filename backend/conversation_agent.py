from llm_client import call_llm_text


MAX_CHAT_MESSAGES = 10


def start_agent_conversation(candidate, parsed_jd):
    name = candidate.get("name", "Candidate")
    job_title = parsed_jd.get("job_title", "the role")

    first_message = (
        f"Hi {name}, I’m ScoutAI, an AI recruiting assistant. "
        f"Your profile appears to match our {job_title} role. "
        f"I would like to ask a few quick questions to understand your genuine interest. "
        f"Are you currently open to exploring this opportunity?"
    )

    return {
        "speaker": "Agent",
        "message": first_message
    }


def generate_next_agent_reply(candidate, parsed_jd, conversation):
    if len(conversation) >= MAX_CHAT_MESSAGES:
        return {
            "speaker": "Agent",
            "message": (
                "Thank you for your responses. I have enough information to "
                "assess your interest and share your profile with the recruiter."
            )
        }

    remaining_messages = MAX_CHAT_MESSAGES - len(conversation)

    prompt = f"""
You are ScoutAI, a professional AI recruiting agent.

Your job is to converse with a candidate and assess genuine interest.

Important rules:
- Ask only ONE question at a time.
- Do not repeat questions already answered.
- Do not continue forever.
- The full conversation must finish within 10 total chat messages.
- Current total messages: {len(conversation)}
- Remaining messages allowed: {remaining_messages}

You need to collect:
1. Whether the candidate is interested
2. Role motivation
3. Location or work-mode comfort
4. Availability or joining timeline
5. Compensation expectation if relevant
6. Skill confirmation based on the JD

If enough information has been collected, or if the conversation is close to 10 messages, wrap up politely and say you will share the profile with the recruiter.

Do not sound robotic.

Candidate Profile:
{candidate}

Job Description Data:
{parsed_jd}

Conversation so far:
{conversation}

Now generate the next agent message only.
"""

    message = call_llm_text(prompt)

    return {
        "speaker": "Agent",
        "message": message
    }


def score_interest_locally(conversation):
    full_text = " ".join(
        item.get("message", "") for item in conversation
    ).lower()

    score = 40
    positive_signals = []
    concerns = []

    if any(word in full_text for word in [
        "yes", "interested", "open", "explore", "sounds good", "excited"
    ]):
        score += 20
        positive_signals.append("Candidate expressed interest in the role.")

    if any(word in full_text for word in [
        "remote", "hybrid", "bangalore", "chennai", "relocate",
        "location works", "comfortable with location"
    ]):
        score += 15
        positive_signals.append("Candidate showed location or work-mode flexibility.")

    if any(word in full_text for word in [
        "immediate", "30 days", "15 days", "join", "available",
        "notice period", "after graduation"
    ]):
        score += 15
        positive_signals.append("Candidate gave availability or joining timeline signal.")

    if any(word in full_text for word in [
        "python", "sql", "azure", "power bi", "machine learning",
        "etl", "api", "pandas", "numpy", "scikit"
    ]):
        score += 10
        positive_signals.append("Candidate confirmed relevant technical skills.")

    if any(word in full_text for word in [
        "not interested", "not looking", "not open", "cannot",
        "not comfortable", "no longer interested"
    ]):
        score -= 25
        concerns.append("Candidate showed hesitation or lack of interest.")

    if "salary" in full_text or "compensation" in full_text or "package" in full_text:
        positive_signals.append("Candidate discussed compensation expectations or constraints.")

    score = max(0, min(score, 100))

    if score >= 80:
        interest_level = "High"
        recommended_action = "Schedule recruiter screening"
    elif score >= 60:
        interest_level = "Medium"
        recommended_action = "Recruiter review recommended"
    else:
        interest_level = "Low"
        recommended_action = "Keep warm or deprioritize"

    if not positive_signals:
        positive_signals.append("Candidate has started the conversation but stronger interest signals are not yet available.")

    return {
        "interest_score": score,
        "interest_level": interest_level,
        "summary": "Interest score calculated from the candidate's real chat responses.",
        "positive_signals": positive_signals,
        "concerns": concerns,
        "recommended_action": recommended_action
    }