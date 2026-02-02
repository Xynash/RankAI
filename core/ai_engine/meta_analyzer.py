def meta_analysis(title, description):
    return {
        "title_length": len(title),
        "description_length": len(description),
        "title_optimal": 30 <= len(title) <= 60,
        "description_optimal": 120 <= len(description) <= 160
    }
