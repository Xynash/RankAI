def ai_visibility(audit_score, semantic_score):
    visibility = (audit_score * 0.6) + (semantic_score * 0.4)

    return {
        "visibility_score": round(visibility, 2),
        "status": "High" if visibility > 75 else "Medium" if visibility > 55 else "Low",
        "prompt_visibility": {
            "search_intent": "Strong" if semantic_score > 60 else "Weak",
            "content_clarity": "Clear" if audit_score > 70 else "Needs Improvement",
            "keyword_coverage": "Good" if visibility > 65 else "Poor"
        }
    }

