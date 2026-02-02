def seo_ranking_overview(seo_score, keyword_count, word_count):
    """
    Rule-based SEO ranking estimation
    (No external APIs, no AI keys)
    """

    # Estimated monthly traffic (very rough heuristic)
    estimated_traffic = (
        seo_score * 15 +
        keyword_count * 120 +
        min(word_count, 2000) * 0.5
    )

    return {
        "visibility": f"{seo_score}%",
        "top_keywords": keyword_count,
        "estimated_traffic": int(estimated_traffic)
    }