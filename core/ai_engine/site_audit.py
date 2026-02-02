def site_audit(html):
    audit = {
        "meta_description": {"status": "Missing"},
        "mobile_responsive": {"status": "Unknown"},
        "page_speed": {"status": "Average"},
        "broken_links": {"status": "Clean"},
    }

    score = 0

    if "<meta name=\"description\"" in html.lower():
        audit["meta_description"]["status"] = "Good"
        score += 25

    # Mobile responsiveness (basic heuristic)
    if "viewport" in html.lower():
        audit["mobile_responsive"]["status"] = "Good"
        score += 25

    # Page speed placeholder
    score += 15

    # Broken links placeholder
    score += 10

    return {
        "score": score,
        "audit": audit
    }


