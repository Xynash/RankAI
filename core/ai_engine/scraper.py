import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def scrape_website(url):
    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)

        if response.status_code != 200:
            return {
                "error": f"HTTP {response.status_code}",
                "html": ""
            }

        soup = BeautifulSoup(response.text, "html.parser")

        # BASIC SEO
        title = soup.title.get_text(strip=True) if soup.title else ""

        meta_desc_tag = soup.find("meta", attrs={"name": "description"})
        meta_desc = (
            meta_desc_tag.get("content", "").strip()
            if meta_desc_tag else ""
        )

        # HEADINGS
        h1 = [h.get_text(strip=True) for h in soup.find_all("h1")]
        h2 = [h.get_text(strip=True) for h in soup.find_all("h2")]

        # LINKS
        internal_links = []
        external_links = []

        domain = urlparse(url).netloc

        for a in soup.find_all("a", href=True):
            href = a["href"].strip()

            if href.startswith("#") or href.startswith("mailto:"):
                continue

            full_url = urljoin(url, href)
            link_domain = urlparse(full_url).netloc

            if domain == link_domain:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)

        # REMOVE SCRIPT & STYLE TEXT
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text = soup.get_text(separator=" ", strip=True)
        word_count = len(text.split())

        return {
            "url": url,
            "title": title,
            "meta_description": meta_desc,
            "html": response.text,

            "h1": h1,
            "h2": h2,

            "internal_links": len(set(internal_links)),
            "external_links": len(set(external_links)),
            "word_count": word_count,
            
            "title_length": len(soup.title.text) if soup.title else 0,
        "meta_desc_length": len(
            soup.find("meta", attrs={"name": "description"})["content"]
        ) if soup.find("meta", attrs={"name": "description"}) else 0,
        "h1_count": len(soup.find_all("h1")),
        "img_without_alt": len([img for img in soup.find_all("img") if not img.get("alt")]),
        "internal_links": len(soup.find_all("a", href=True)),
        }

    except Exception as e:
        return {
            "error": str(e),
            "html": ""
        }
