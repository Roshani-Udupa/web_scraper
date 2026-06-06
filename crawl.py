from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from typing import TypedDict

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(url: str) -> str:
    parsed = urlparse(url)

    netloc = parsed.netloc.lower()

    path = parsed.path.rstrip('/')
    return f"{netloc}{path}"

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("h1"):
        return soup.h1.get_text()
    elif soup.find("h2"):
        return soup.h2.get_text()
    else:
        return ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("main") and soup.find("main").find("p"):
        return soup.main.p.get_text()
    elif soup.find("p"):
        return soup.p.get_text()
    else:
        return ""

def get_urls_from_html(html:str, base_url:str)->list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    links_url = []
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href:
            abs_url = urljoin(base_url, href)
            links_url.append(abs_url)
    return links_url

def get_images_from_html(html:str, base_url:str)->list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    image_urls = []
    images = soup.find_all("img")
    for image in images:
        src = image.get("src")
        if src:
            abs_url = urljoin(base_url, src)
            image_urls.append(abs_url)
    
    return image_urls

def extract_page_data(html: str, page_url: str) -> PageData:
    heading = get_heading_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    outgoing_links = get_urls_from_html(html, page_url)
    image_urls = get_images_from_html(html, page_url)

    return {
        "url": page_url,
        "heading": heading,
        "first_paragraph": first_paragraph,
        "outgoing_links": outgoing_links,
        "image_urls": image_urls,
    }