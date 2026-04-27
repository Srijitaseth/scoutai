import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def safe_join(items):
    if not items:
        return "None"
    if isinstance(items, list):
        return ", ".join(str(item) for item in items)
    return str(items)


def normalize_text(value):
    if not value:
        return "Not available"
    return str(value)


def summarize_education(parsed_resume):
    education = parsed_resume.get("education", [])

    if not education:
        return "No education details found."

    summaries = []

    for item in education[:2]:
        if isinstance(item, dict):
            degree = item.get("degree", "")
            institution = item.get("institution", "")
            duration = item.get("duration", "")
            score = item.get("score", "")

            parts = [degree, institution, duration, score]
            summary = " | ".join(part for part in parts if part)
            if summary:
                summaries.append(summary)
        else:
            summaries.append(str(item))

    return "; ".join(summaries) if summaries else "No education details found."


def summarize_experience(parsed_resume):
    experience = parsed_resume.get("experience", [])

    if not experience:
        return "No experience details found."

    summaries = []

    for item in experience[:2]:
        if isinstance(item, dict):
            role = item.get("role", "")
            company = item.get("company", "")
            duration = item.get("duration", "")
            highlights = item.get("highlights", [])

            highlight_text = ""
            if isinstance(highlights, list) and highlights:
                highlight_text = highlights[0]

            parts = [role, company, duration, highlight_text]
            summary = " | ".join(part for part in parts if part)
            if summary:
                summaries.append(summary)
        else:
            summaries.append(str(item))

    return "; ".join(summaries) if summaries else "No experience details found."


def summarize_projects(parsed_resume):
    projects = parsed_resume.get("projects", [])

    if not projects:
        return "No project details found."

    summaries = []

    for item in projects[:2]:
        if isinstance(item, dict):
            name = item.get("name", "")
            technologies = safe_join(item.get("technologies", []))
            highlights = item.get("highlights", [])

            highlight_text = ""
            if isinstance(highlights, list) and highlights:
                highlight_text = highlights[0]

            parts = [name, technologies, highlight_text]
            summary = " | ".join(part for part in parts if part)
            if summary:
                summaries.append(summary)
        else:
            summaries.append(str(item))

    return "; ".join(summaries) if summaries else "No project details found."


def summarize_conversation(candidate):
    conversation = candidate.get("conversation", [])

    if not conversation:
        return "Conversation not started."

    candidate_replies = [
        item.get("message", "")
        for item in conversation
        if item.get("speaker") == "Candidate"
    ]

    if not candidate_replies:
        return "Candidate has not replied yet."

    return " | ".join(candidate_replies[:3])


def bullet_paragraphs(items, style):
    if not items:
        return [Paragraph("• None", style)]

    paragraphs = []
    for item in items:
        paragraphs.append(Paragraph(f"• {normalize_text(item)}", style))
    return paragraphs


def export_csv(candidates, file_path):
    headers = [
        "Rank",
        "Name",
        "Email",
        "Match Score",
        "Interest Score",
        "Interest Level",
        "Final Score",
        "Matched Skills",
        "Missing Skills",
        "Why Matched",
        "Education Summary",
        "Experience Summary",
        "Project Summary",
        "Conversation Summary",
        "Positive Signals",
        "Concerns",
        "Recruiter Feedback",
        "Recommended Action",
    ]

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for index, candidate in enumerate(candidates, start=1):
            parsed_resume = candidate.get("parsed_resume", {})

            writer.writerow({
                "Rank": index,
                "Name": candidate.get("name", ""),
                "Email": candidate.get("email", ""),
                "Match Score": candidate.get("match_score", ""),
                "Interest Score": candidate.get("interest_score", ""),
                "Interest Level": candidate.get("interest_level", "Not assessed"),
                "Final Score": candidate.get("final_score", ""),
                "Matched Skills": safe_join(candidate.get("matched_skills", [])),
                "Missing Skills": safe_join(candidate.get("missing_skills", [])),
                "Why Matched": safe_join(candidate.get("explanation", [])),
                "Education Summary": summarize_education(parsed_resume),
                "Experience Summary": summarize_experience(parsed_resume),
                "Project Summary": summarize_projects(parsed_resume),
                "Conversation Summary": summarize_conversation(candidate),
                "Positive Signals": safe_join(candidate.get("positive_signals", [])),
                "Concerns": safe_join(candidate.get("concerns", [])),
                "Recruiter Feedback": candidate.get("recruiter_feedback", "Not reviewed"),
                "Recommended Action": candidate.get("recommended_action", ""),
            })


def export_pdf(candidates, file_path):
    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=14,
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading3"],
        fontSize=12,
        leading=14,
        textColor=colors.HexColor("#1d4ed8"),
        spaceBefore=8,
        spaceAfter=6,
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#111827"),
        spaceAfter=4,
    )

    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#374151"),
        spaceAfter=3,
    )

    candidate_header_style = ParagraphStyle(
        "CandidateHeader",
        parent=styles["Heading2"],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#111827"),
        spaceAfter=8,
    )

    story = []

    story.append(Paragraph("ScoutAI - Ranked Candidate Shortlist", title_style))
    story.append(
        Paragraph(
            "Recruiter-ready summary of shortlisted candidates with scores, fit analysis, profile snapshot, and engagement insights.",
            normal_style,
        )
    )
    story.append(Spacer(1, 12))

    for index, candidate in enumerate(candidates, start=1):
        parsed_resume = candidate.get("parsed_resume", {})

        story.append(
            Paragraph(
                f"Rank {index} — {normalize_text(candidate.get('name', 'Unknown Candidate'))}",
                candidate_header_style,
            )
        )

        story.append(
            Paragraph(
                f"<b>Email:</b> {normalize_text(candidate.get('email', 'Not available'))}",
                normal_style,
            )
        )

        # Score summary table
        score_data = [
            ["Match Score", candidate.get("match_score", "0"), "Interest Score", candidate.get("interest_score", "0")],
            ["Final Score", candidate.get("final_score", "0"), "Interest Level", candidate.get("interest_level", "Not assessed")],
            ["Recruiter Feedback", candidate.get("recruiter_feedback", "Not reviewed"), "Recommended Action", candidate.get("recommended_action", "Not assigned")],
        ]

        score_table = Table(score_data, colWidths=[1.4 * inch, 1.2 * inch, 1.6 * inch, 2.2 * inch])
        score_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#111827")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#94a3b8")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(score_table)
        story.append(Spacer(1, 10))

        # Skills snapshot
        story.append(Paragraph("Skills Snapshot", section_style))

        skills_table = Table(
            [
                [
                    Paragraph("<b>Matched Skills</b>", normal_style),
                    Paragraph("<b>Missing Skills</b>", normal_style),
                ],
                [
                    Paragraph(normalize_text(safe_join(candidate.get("matched_skills", []))), small_style),
                    Paragraph(normalize_text(safe_join(candidate.get("missing_skills", []))), small_style),
                ],
            ],
            colWidths=[3.2 * inch, 3.2 * inch],
        )

        skills_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#f8fafc")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#94a3b8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(skills_table)
        story.append(Spacer(1, 8))

        # Why matched
        story.append(Paragraph("Why Matched", section_style))
        for para in bullet_paragraphs(candidate.get("explanation", []), small_style):
            story.append(para)

        story.append(Spacer(1, 8))

        # Profile snapshot
        story.append(Paragraph("Profile Snapshot", section_style))

        story.append(
            Paragraph(
                f"<b>Education:</b> {normalize_text(summarize_education(parsed_resume))}",
                small_style,
            )
        )
        story.append(
            Paragraph(
                f"<b>Experience:</b> {normalize_text(summarize_experience(parsed_resume))}",
                small_style,
            )
        )
        story.append(
            Paragraph(
                f"<b>Projects:</b> {normalize_text(summarize_projects(parsed_resume))}",
                small_style,
            )
        )

        story.append(Spacer(1, 8))

        # Engagement insights
        story.append(Paragraph("Engagement Insights", section_style))

        story.append(
            Paragraph(
                f"<b>Conversation Summary:</b> {normalize_text(summarize_conversation(candidate))}",
                small_style,
            )
        )

        story.append(
            Paragraph(
                f"<b>Positive Signals:</b> {normalize_text(safe_join(candidate.get('positive_signals', [])))}",
                small_style,
            )
        )

        story.append(
            Paragraph(
                f"<b>Concerns:</b> {normalize_text(safe_join(candidate.get('concerns', [])))}",
                small_style,
            )
        )

        if index != len(candidates):
            story.append(Spacer(1, 16))
            story.append(PageBreak())

    doc.build(story)