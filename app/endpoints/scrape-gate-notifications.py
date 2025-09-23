import requests
from bs4 import BeautifulSoup

def get_gate_notifications():
    url = "https://gate.iitk.ac.in/"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    notifications = []
 
    for marquee in soup.find_all("marquee"):
        for anchor in marquee.find_all("a"):
            title = anchor.get_text(strip=True)
            link = anchor.get("href")
            if link and not link.startswith("http"):
                link = url + link.lstrip("/")
            notifications.append({"title": title, "link": link})


    for li in soup.select(".news-update li, .news-list li"):
        anchor = li.find("a")
        title = anchor.get_text(strip=True) if anchor else li.get_text(strip=True)
        link = anchor.get("href") if anchor else url
        if link and not link.startswith("http"):
            link = url + link.lstrip("/")
        notifications.append({"title": title, "link": link})

    return notifications

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_gate_notifications())
