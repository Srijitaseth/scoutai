def generate_dashboard_data(candidates):
    total = len(candidates)

    if total == 0:
        return {
            "total_candidates": 0,
            "average_match_score": 0,
            "average_interest_score": 0,
            "top_candidate": None,
            "chart_data": []
        }

    average_match = sum(c["match_score"] for c in candidates) / total
    average_interest = sum(c["interest_score"] for c in candidates) / total

    top_candidate = max(candidates, key=lambda x: x["final_score"])

    chart_data = [
        {
            "name": c["name"],
            "matchScore": c["match_score"],
            "interestScore": c["interest_score"],
            "finalScore": c["final_score"]
        }
        for c in candidates
    ]

    return {
        "total_candidates": total,
        "average_match_score": round(average_match, 2),
        "average_interest_score": round(average_interest, 2),
        "top_candidate": top_candidate["name"],
        "chart_data": chart_data
    }