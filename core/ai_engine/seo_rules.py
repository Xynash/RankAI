def rule_based_score(title, meta, h1, words, load_time):
    score = 0

    if 50 <= len(title) <= 60:
        score += 15
    if 120 <= len(meta) <= 160:
        score += 15
    if h1 == 1:
        score += 10
    if words > 500:
        score += 20
    if load_time < 3:
        score += 10

    return min(score, 70)

def calculate_seo_score(features):
    score = 100

    if features["title_length"] < 30:
        score -= 10

    if features["meta_desc_length"] < 70:
        score -= 10

    if features["h1_count"] != 1:
        score -= 10

    if features["img_without_alt"] > 5:
        score -= 15

    return max(score, 0)

