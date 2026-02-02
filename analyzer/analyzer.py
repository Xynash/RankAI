from django.http import JsonResponse
from core.ai_engine.scraper import scrape_website
from core.ai_engine.site_audit import site_audit
from core.ai_engine.semantic import semantic_score
from core.ai_engine.keywords_ai import recommended_keywords
from core.ai_engine.ai_visibility import ai_visibility
from core.ai_engine.tracking import tracking_overview
from core.ai_engine.seo_rules import rule_based_score , calculate_seo_score
from core.ai_engine.seo_ranking import seo_ranking_overview
from core.ai_engine.issues_knowledge import ISSUE_KNOWLEDGE 

from bs4 import BeautifulSoup

def extract_features(html):
    soup = BeautifulSoup(html, "html.parser")
    return {
          "title_length": len(soup.title.text) if soup.title else 0,
        "meta_desc_length": len(
            soup.find("meta", attrs={"name": "description"})["content"]
        ) if soup.find("meta", attrs={"name": "description"}) else 0,
        "h1_count": len(soup.find_all("h1")),
        "img_without_alt": len(
            [img for img in soup.find_all("img") if not img.get("alt")]
        ),
        "internal_links": len(soup.find_all("a", href=True)),
    }


def detect_issues(features):
    issues = []

    if features["img_without_alt"] > 0:
        knowledge = ISSUE_KNOWLEDGE["Image Alt Attributes"]
        issues.append({
            "type": "warning",
            "title": "Image Alt Attributes",
            "count": features["img_without_alt"],
            "description":  (
            f'{features["img_without_alt"]} images are missing ALT text, '
            'reducing accessibility and image search visibility.'
        ),
            "theory": knowledge["theory"],
            "mitigation": knowledge["mitigation"]
        })

    if features["title_length"] < 30:
        issues.append({
            "type": "critical",
            "title": "Title Tag Too Short",
            "count": 1,
            "description": "Title tag length is below SEO standards",
            "mitigation": "Increase title length to 50–60 characters."
        })

    return issues

def analyze_api(request):
    url = request.GET.get("url")

    if not url:
        return JsonResponse({"error": "URL is required"}, status=400)

    # ========= SCRAPE =========
    data = scrape_website(url)
    html = data.get("html", "")
    title = data.get("title", "")
    meta_desc = data.get("meta_description", "")

    # ========= SITE AUDIT =========
    raw_audit = site_audit(html) if html else {"score": 0}

    audit = {
        "score": raw_audit.get("score", 0),
        "audit": {
            "meta_description": {
                "status": "Good" if meta_desc else "Missing"
            },
            "mobile_responsive": {
                "status": "Unknown"
            },
            "page_speed": {
                "status": "Average"
            },
            "broken_links": {
                "status": "Clean"
            }
        }
    }

    # ========= SEMANTIC =========
    semantic = semantic_score(f"{title} {meta_desc}")

    # ========= AI KEYWORDS =========
    keywords = recommended_keywords(f"{title} {meta_desc}")

    # ========= VISIBILITY =========
    visibility = ai_visibility(
        audit["score"],
        semantic.get("semantic_score", 0)
    )

    visibility["prompt_visibility"] = {
        "search_intent": "Strong" if semantic["semantic_score"] > 50 else "Weak",
        "content_clarity": "Good" if audit["score"] > 60 else "Needs Improvement",
        "keyword_coverage": "Good" if len(keywords) >= 5 else "Poor"
    }
    # ========= SEO RANKING OVERVIEW =========
    seo_ranking = seo_ranking_overview(
    seo_score=visibility["visibility_score"],
    keyword_count=len(keywords),
    word_count=len(html)
)



    # ========= TRACKING =========
    tracking = tracking_overview()
    tracking.update({
        "estimated_traffic": 1200,
        "llm_visibility": 78,
        "chatgpt": 82,
        "perplexity": 65,
        "claude": 71
    })
    
     # ✅ NEW PART (THIS IS WHAT YOU ASKED ABOUT)
    features = extract_features(html)
    issues = detect_issues(features)

    report = {
        "url": url,
        "features": features,
        "issues": issues,
        
    }

    request.session["analysis_data"] = report

    # ========= RESPONSE =========
    return JsonResponse({
        "url": url,
        "seo_score": visibility["visibility_score"],
        "site_audit": audit,
        "semantic_effectiveness": semantic,
        "recommended_keywords": keywords,  
        "ai_visibility": visibility,
        "seo_ranking_overview": seo_ranking,
        "tracking_overview": tracking,
        "report":report
    })


###################################################


