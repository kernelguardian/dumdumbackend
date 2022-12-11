from urllib.parse import urlparse


def is_youtube_url(url: str) -> bool:
    parsed_url = urlparse(url)
    if parsed_url.hostname == "www.youtube.com":
        return True
    return False
