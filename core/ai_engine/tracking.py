def tracking_overview():
    max_traffic = 20000
    traffic = 12000

    return {
        "estimated_traffic": traffic,
        "traffic_percent": int((traffic / max_traffic) * 100),
        "llm_visibility": 78,
        "chatgpt": 72,
        "perplexity": 65,
        "claude": 60
    }

