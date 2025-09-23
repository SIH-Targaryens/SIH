import requests
from bs4 import BeautifulSoup

def get_nta_notifications():
    url = "https://nta.ac.in/whatsnew"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    notifications = []
    
    for li in soup.select(".news-list li"):
        title_tag = li.find(class_="news-title")
        title = title_tag.text.strip() if title_tag else li.get_text(strip=True)
        link_tag = li.find("a")
        link = link_tag["href"] if link_tag else url
        if link and not link.startswith("http"):
            link = f"https://nta.ac.in{link}"
        date_tag = li.find(class_="news-date")
        date = date_tag.text.strip() if date_tag else ""
        notifications.append({
            "title": title,
            "link": link,
            "date": date
        })
    return notifications

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_nta_notifications())
