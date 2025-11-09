# scraper.py
import requests
from bs4 import BeautifulSoup
from typing import Dict

def scrape_wikipedia(url: str) -> Dict:
    """
    Fetch a Wikipedia article and return a dict with title and cleaned text.
    Uses a browser User-Agent to avoid 403s from some hosts.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 (AI-Quiz-Generator/1.0)"
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    title_el = soup.find(id="firstHeading")
    title = title_el.get_text(strip=True) if title_el else (soup.title.string if soup.title else "")

    # Main content paragraphs (Wikipedia layout)
    content = soup.select("div.mw-parser-output > p")
    paragraphs = [p.get_text(" ", strip=True) for p in content if p.get_text(strip=True)]
    if not paragraphs:
        # fallback to any <p>
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]

    text = "\n\n".join(paragraphs).strip()
    if not text:
        raise RuntimeError("No article text extracted from URL")

    return {"url": url, "title": title, "text": text}
