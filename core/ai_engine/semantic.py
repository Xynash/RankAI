def semantic_score(text):
    words = text.lower().split()
    unique_words = set(words)

    diversity = len(unique_words) / max(len(words), 1)

    score = round(diversity * 100, 2)

    return {
        "semantic_score": score,
        "unique_terms": len(unique_words),
        "total_terms": len(words)
    }
