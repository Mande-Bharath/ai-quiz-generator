import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch Wikipedia page.")
    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.find("div", {"id": "mw-content-text"})
    text = content_div.get_text(separator="\n", strip=True)
    return text
