from urllib.parse import urlparse
def normalize_url(url: str) -> str:
    parsed = urlparse(url)

    netloc = parsed.netloc.lower()

    path = parsed.path.rstrip('/')
    return f"{netloc}{path}"
